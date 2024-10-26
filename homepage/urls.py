import uuid

from django.conf import settings
from django.urls import path, register_converter

from .views import index, article, media


class UUIDConverter:
    regex = r'[0-9a-f]{32}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

    @staticmethod
    def to_python(value):
        return uuid.UUID(value)

    @staticmethod
    def to_url(value):
        return str(value)


register_converter(UUIDConverter, 'uuid')

urlpatterns = [
    path('', index, name='index'),
    path('article/<uuid:identifier>/', article, name='article'),
]

if not settings.DEBUG:
    urlpatterns.append(path('media/<path:path>', media, name='media'))
