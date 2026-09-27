import re
from PIL import Image

from django.core.exceptions import ValidationError


MAX_IMAGE_SIZE = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 25_000_000


def validate_hex_color(value):
    if not re.fullmatch(r'#[0-9A-Fa-f]{6}', value):
        raise ValidationError(f'{value} is not a valid hex color code')


def validate_image_upload(value):
    if value.size > MAX_IMAGE_SIZE:
        raise ValidationError('Images must be 10 MB or smaller.')

    position = value.tell() if hasattr(value, 'tell') else None
    try:
        with Image.open(value) as image:
            width, height = image.size
            if width * height > MAX_IMAGE_PIXELS:
                raise ValidationError('Images may contain at most 25 megapixels.')
            image.verify()
    except (Image.DecompressionBombError, OSError, SyntaxError) as exc:
        raise ValidationError('Upload a valid, non-corrupt image.') from exc
    finally:
        if position is not None:
            value.seek(position)
