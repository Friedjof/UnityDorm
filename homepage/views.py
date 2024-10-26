from django.shortcuts import render

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
