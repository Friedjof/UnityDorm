from django.core.management.base import BaseCommand

from homepage.images import optimized_image
from homepage.models import Article, Shortcut


class Command(BaseCommand):
    help = 'Generate the responsive image variants used by the frontend.'

    def handle(self, *args, **options):
        generated = 0

        shortcuts = Shortcut.objects.exclude(image='').exclude(image__isnull=True).iterator()
        for shortcut in shortcuts:
            if optimized_image(shortcut.image, 200, 200).url:
                generated += 1

        articles = Article.objects.exclude(image='').exclude(image__isnull=True).iterator()
        for article in articles:
            for width, height in (
                (360, 180),
                (720, 360),
                (640, 300),
                (1280, 600),
                (1920, 900),
            ):
                if optimized_image(article.image, width, height).url:
                    generated += 1

        self.stdout.write(self.style.SUCCESS(f'Image cache ready ({generated} variants).'))
