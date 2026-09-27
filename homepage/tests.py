import shutil
import tempfile
from io import BytesIO

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404
from django.test import RequestFactory, TestCase, override_settings
from PIL import Image

from .images import optimized_image
from .admin import ArticleAdmin
from .models import Article, ArticleCategory, Author, Shortcut
from .views import media


def uploaded_image(name='test.png', size=(1200, 800), color='#20524f'):
    output = BytesIO()
    Image.new('RGB', size, color).save(output, format='PNG')
    return SimpleUploadedFile(name, output.getvalue(), content_type='image/png')


class HomepageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.media_root = tempfile.mkdtemp(prefix='unitydorm-tests-')
        cls.settings_override = override_settings(MEDIA_ROOT=cls.media_root)
        cls.settings_override.enable()

    @classmethod
    def tearDownClass(cls):
        cls.settings_override.disable()
        shutil.rmtree(cls.media_root)
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username='author')
        author = Author.objects.create(user=self.user)
        category = ArticleCategory.objects.create(name='News')
        self.article = Article.objects.create(
            title='Published article',
            description='Description',
            article=(
                '[unsafe](javascript:alert(1))\n\n'
                '<script>alert("xss")</script>\n\n'
                '![remote](https://example.com/image.png)'
            ),
            image=uploaded_image(),
            published=True,
            category=category,
        )
        self.article.authors.add(author)

    def test_homepage_uses_responsive_cached_images(self):
        Shortcut.objects.create(
            title='Example', url='https://example.com', image=uploaded_image('shortcut.png')
        )

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'srcset=')
        self.assertContains(response, '/media/optimized/')
        self.assertContains(response, 'loading="lazy"')

    def test_missing_optional_images_do_not_break_homepage(self):
        Shortcut.objects.create(title='No image', url='https://example.com')
        self.article.image.delete(save=True)

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No image')

    def test_derivative_is_resized_webp_and_reused(self):
        first = optimized_image(self.article.image, 360, 180)
        second = optimized_image(self.article.image, 360, 180)

        self.assertEqual(first, second)
        self.assertEqual((first.width, first.height), (360, 180))
        self.assertTrue(first.url.endswith('.webp'))
        path = first.url.removeprefix('/media/')
        with open(f'{self.media_root}/{path}', 'rb') as image_file:
            with Image.open(image_file) as image:
                self.assertEqual(image.format, 'WEBP')
                self.assertEqual(image.size, (360, 180))

    def test_article_sanitizes_rendered_markdown(self):
        response = self.client.get(f'/article/{self.article.identifier}/')
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('javascript:', content)
        self.assertNotIn('<script>alert', content)
        self.assertIn('loading="lazy" decoding="async"', content)

    def test_unpublished_article_is_not_public(self):
        self.article.published = False
        self.article.save(update_fields=['published'])

        response = self.client.get(f'/article/{self.article.identifier}/')

        self.assertEqual(response.status_code, 404)

    def test_non_superuser_admin_only_sees_own_articles(self):
        other_user = User.objects.create_user(username='other-author')
        other_author = Author.objects.create(user=other_user)
        other_article = Article.objects.create(
            title='Other article',
            description='Private to the other author',
            article='Content',
            published=False,
            category=self.article.category,
        )
        other_article.authors.add(other_author)
        request = RequestFactory().get('/admin/homepage/article/')
        request.user = self.user

        queryset = ArticleAdmin(Article, admin.site).get_queryset(request)

        self.assertQuerySetEqual(queryset, [self.article])

    def test_media_response_uses_cache_and_nosniff_headers(self):
        derivative = optimized_image(self.article.image, 360, 180)
        path = derivative.url.removeprefix('/media/')

        response = media(RequestFactory().get(derivative.url), path)

        self.assertIn('max-age=31536000', response['Cache-Control'])
        self.assertIn('immutable', response['Cache-Control'])
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        response.close()

    def test_media_view_rejects_path_traversal(self):
        with self.assertRaises(Http404):
            media(RequestFactory().get('/media/../settings.py'), '../settings.py')
