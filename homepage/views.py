import os
from PIL import Image

from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse, Http404

import bleach
from markdown import markdown

from .models import Shortcut, Article

def index(request):
    return render(request, 'homepage/index.html', {
        'title': 'Welcome to UnityDorm', 'shortcuts': Shortcut.objects.all(), 'articles': Article.objects.all()
    })


def article(request, identifier):
    try:
        a = Article.objects.get(identifier=identifier)
    except Article.DoesNotExist:
        return render(request, 'homepage/404.html', {'title': 'Article not found'})

    return render(request, 'homepage/article.html', {
        'article': a, 'title': a.title,
        'content': markdown(bleach.clean(a.article, tags=['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'u', 's', 'a', 'img', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre'], attributes={'a': ['href'], 'img': ['src', 'alt']}))
    })


def media(request, path):
    media_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, path))

    if os.path.commonpath([media_path, settings.MEDIA_ROOT]) != str(settings.MEDIA_ROOT):
        raise Http404("Media not found")

    if os.path.exists(media_path):
        try:
            with Image.open(media_path) as img:
                img.verify()  # Verify that this is an image
            return FileResponse(open(media_path, 'rb'))
        except (IOError, SyntaxError) as e:
            raise Http404("Media not found")
    else:
        raise Http404("Media not found")
