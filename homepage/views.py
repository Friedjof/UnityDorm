import os
import mimetypes
import re

from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils._os import safe_join
from django.utils.cache import patch_cache_control
from django.views.decorators.http import require_GET

import bleach
from markdown import markdown

from .models import Shortcut, Article


def index(request):
    return render(request, 'homepage/index.html', {
        'title': 'Welcome to UnityDorm',
        'shortcuts': Shortcut.objects.all().order_by('order'),
        'articles': Article.objects.filter(published=True).select_related('category').order_by('-date')[:10]
    })


def article(request, identifier):
    a = get_object_or_404(
        Article.objects.select_related('category'),
        identifier=identifier,
        published=True,
    )
    rendered_markdown = markdown(a.article)
    clean_content = bleach.clean(
        rendered_markdown,
        tags=[
            'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'u', 's',
            'a', 'img', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'br', 'hr',
        ],
        attributes={
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'title'],
        },
        protocols={'http', 'https', 'mailto'},
        strip=True,
    )
    clean_content = re.sub(
        r'<img(?=\s)',
        '<img loading="lazy" decoding="async" referrerpolicy="no-referrer"',
        clean_content,
    )

    return render(request, 'homepage/article.html', {
        'article': a, 'title': a.title,
        'content': clean_content,
    })


@require_GET
def media(request, path):
    try:
        media_path = safe_join(settings.MEDIA_ROOT, path)
    except (SuspiciousFileOperation, ValueError):
        raise Http404("Media not found")

    if not os.path.isfile(media_path):
        raise Http404("Media not found")

    content_type, _ = mimetypes.guess_type(media_path)
    response = FileResponse(open(media_path, 'rb'), content_type=content_type)
    if path.startswith('optimized/'):
        patch_cache_control(response, public=True, max_age=31536000, immutable=True)
    else:
        patch_cache_control(response, public=True, max_age=86400)
    response['X-Content-Type-Options'] = 'nosniff'
    return response
