from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Shortcut, Article, ArticleCategory, Author


class ShortcutResource(resources.ModelResource):
    class Meta:
        model = Shortcut
        fields = ('order', 'identifier', 'title', 'url', 'image', 'new_tab', 'color', 'background')
        import_id_fields = ('identifier',)
        export_order = ('identifier', 'order', 'title', 'url', 'image', 'new_tab', 'color', 'background')


# Register your models here.
@admin.register(Shortcut)
class ShortcutAdmin(ImportExportModelAdmin):
    resource_class = ShortcutResource

    list_display = ('title', 'url', 'order', 'new_tab', 'color', 'background')
    search_fields = ('title', 'url')
    ordering = ('order',)
    list_filter = ('new_tab',)

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            if request.user.is_superuser:
                return True
            return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if obj is not None:
            return True
        return super().has_view_permission(request, obj)


class ArticleCategoryResource(resources.ModelResource):
    class Meta:
        model = ArticleCategory
        fields = ('identifier', 'name', 'color', 'background')
        import_id_fields = ('identifier',)
        export_order = ('identifier', 'name', 'color', 'background')


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(ImportExportModelAdmin):
    resource_class = ArticleCategoryResource

    list_display = ('name', 'color', 'background')
    search_fields = ('name',)
    ordering = ('name',)

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            if request.user.is_superuser:
                return True
            return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if obj is not None:
            return True
        return super().has_view_permission(request, obj)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'registered')
    search_fields = ('user__username', 'user__email')
    ordering = ('-registered',)

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            if request.user.is_superuser:
                return True
            return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if obj is not None:
            return True
        return super().has_view_permission(request, obj)


class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article
        fields = ('identifier', 'title', 'description', 'article', 'image', 'date', 'category')
        import_id_fields = ('identifier',)
        export_order = ('identifier', 'title', 'description', 'article', 'image', 'date', 'category')


@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin):
    resource_class = ArticleResource

    list_display = ('title', 'category', 'date', 'published', 'view_article_link')
    search_fields = ('title', 'description')
    ordering = ('-date',)
    list_filter = ('category', 'published')
    actions = ['publish_articles']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(authors__user=request.user).distinct()

    def view_article_link(self, obj):
        url = f'/article/{obj.identifier}/'
        return format_html('<a href="{}" target="_blank">View Article</a>', url)

    view_article_link.short_description = 'Article Link'

    def publish_articles(self, request, queryset):
        updated_count = queryset.update(published=True)
        self.message_user(request, f'{updated_count} articles were successfully marked as published.')

    publish_articles.short_description = 'Publish selected articles'

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            if request.user.is_superuser or obj.is_author(request.user):
                return True
            return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.is_author(request.user)
        return super().has_view_permission(request, obj)
