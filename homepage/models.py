from uuid import uuid4

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


class ArticleCategory(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=20)

    color = models.CharField(max_length=7, default='#000000', validators=[validate_hex_color])
    background = models.CharField(max_length=7, default='#FFFFFF', validators=[validate_hex_color])

    def __str__(self):
        return self.name


class Article(models.Model):
    identifier = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    title = models.CharField(max_length=42)
    description = models.CharField(max_length=128)
    article = models.TextField()

    image = models.ImageField(upload_to='news/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
