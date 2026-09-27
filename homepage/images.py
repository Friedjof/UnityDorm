"""Helpers for generating cached, browser-friendly image derivatives."""

from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps


@dataclass(frozen=True)
class OptimizedImage:
    url: str
    width: int | None = None
    height: int | None = None


def _cache_name(image_field, width: int, height: int | None) -> str:
    storage = image_field.storage
    try:
        version = storage.get_modified_time(image_field.name).isoformat()
    except (AttributeError, NotImplementedError, OSError):
        version = image_field.name

    key = f"{image_field.name}:{version}:{width}:{height or 0}:v1"
    digest = sha256(key.encode()).hexdigest()[:20]
    stem = Path(image_field.name).stem[:40]
    return f"optimized/{stem}-{digest}-{width}x{height or 0}.webp"


def optimized_image(image_field, width: int, height: int | None = None) -> OptimizedImage:
    """Return a cached WebP derivative, falling back safely to the source image."""
    if not image_field:
        return OptimizedImage("")

    width = max(1, min(int(width), 2560))
    height = max(1, min(int(height), 2560)) if height else None
    storage = image_field.storage
    cache_name = _cache_name(image_field, width, height)

    try:
        if not storage.exists(cache_name):
            with storage.open(image_field.name, "rb") as source:
                with Image.open(source) as original:
                    image = ImageOps.exif_transpose(original)
                    if height:
                        scale = min(1, image.width / width, image.height / height)
                        target_size = (
                            max(1, round(width * scale)),
                            max(1, round(height * scale)),
                        )
                        image = ImageOps.fit(
                            image,
                            target_size,
                            method=Image.Resampling.LANCZOS,
                        )
                    else:
                        image.thumbnail((width, width * 2), Image.Resampling.LANCZOS)

                    if image.mode not in {"RGB", "RGBA"}:
                        image = image.convert("RGBA" if "transparency" in image.info else "RGB")

                    output = BytesIO()
                    image.save(output, format="WEBP", quality=82, method=4)
                    saved_name = storage.save(cache_name, ContentFile(output.getvalue()))
                    cache_name = saved_name

        with storage.open(cache_name, "rb") as cached:
            with Image.open(cached) as image:
                rendered_width, rendered_height = image.size

        return OptimizedImage(
            storage.url(cache_name),
            width=rendered_width,
            height=rendered_height,
        )
    except (FileNotFoundError, Image.DecompressionBombError, OSError, ValueError):
        try:
            return OptimizedImage(image_field.url, image_field.width, image_field.height)
        except (FileNotFoundError, OSError, ValueError):
            return OptimizedImage("")
