from uuid import uuid4
from datetime import datetime

from django.db import models

from .validators import validate_hex_color

# Create your models here.
class Shortcut(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.PositiveIntegerField(default=0, db_index=True)

    title = models.CharField(max_length=24)
    url = models.URLField()
    image = models.ImageField(upload_to='shortcuts/', null=True, blank=True)
    new_tab = models.BooleanField(default=False)

    color = models.CharField(max_length=7, default='#000000', validators=[validate_hex_color])
    background = models.CharField(max_length=7, default='#FFFFFF', validators=[validate_hex_color])

    def __str__(self):
        return self.title


class Author(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class ArticleCategory(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=20)

    color = models.CharField(max_length=7, default='#000000', validators=[validate_hex_color])
    background = models.CharField(max_length=7, default='#FFFFFF', validators=[validate_hex_color])

    def __str__(self):
        return self.name


class Article(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    authors = models.ManyToManyField(Author)

    title = models.CharField(max_length=42)
    description = models.CharField(max_length=128)
    article = models.TextField()

    image = models.ImageField(upload_to='news/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True, editable=False, null=True)

    def is_author(self, user):
        return self.authors.filter(user=user).exists()

    def __str__(self):
        return self.title
