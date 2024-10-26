from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Shortcut, Article, ArticleCategory


class ShortcutResource(resources.ModelResource):
    class Meta:
        model = Shortcut
        fields = ('identifier', 'order', 'title', 'url', 'image', 'new_tab', 'color', 'background')


# Register your models here.
@admin.register(Shortcut)
class ShortcutAdmin(ImportExportModelAdmin):
    resource_class = ShortcutResource

    list_display = ('title', 'url', 'order', 'new_tab', 'color', 'background')
    search_fields = ('title', 'url')
    ordering = ('order',)


class ArticleCategoryResource(resources.ModelResource):
    class Meta:
        model = ArticleCategory
        fields = ('identifier', 'name', 'color', 'background')


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(ImportExportModelAdmin):
    resource_class = ArticleCategoryResource

    list_display = ('name', 'color', 'background')
    search_fields = ('name',)
    ordering = ('name',)


class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article
        fields = ('identifier', 'title', 'description', 'article', 'image', 'date', 'category')


@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin):
    resource_class = ArticleResource

    list_display = ('title', 'category', 'date')
    search_fields = ('title', 'description')
    ordering = ('-date',)
