from django.test import TestCase, override_settings
from django.conf import settings
from unittest import mock
from urllib.error import URLError
from opensec_project.middleware import RateLimitMiddleware
from .models import Category, Resource


class ResourceOrderingTest(TestCase):
    def test_order_by_upvotes(self):
        cat = Category.objects.create(name='TestCat')
        r1 = Resource.objects.create(url='http://a.com', description='A', category=cat, upvotes=1)
        r2 = Resource.objects.create(url='http://b.com', description='B', category=cat, upvotes=5)
        r3 = Resource.objects.create(url='http://c.com', description='C', category=cat, upvotes=3)
        resources = list(Resource.objects.all())
        self.assertEqual(resources[0], r2)
        self.assertEqual(resources[1], r3)
        self.assertEqual(resources[2], r1)


class UpvoteLimitTest(TestCase):
    def test_single_upvote_per_session(self):
        cat = Category.objects.create(name='TestCat2')
        res = Resource.objects.create(url='http://example.com', description='Ex', category=cat)

        response = self.client.get(f'/upvote/{res.pk}/')
        res.refresh_from_db()
        self.assertEqual(res.upvotes, 1)

        response = self.client.get(f'/upvote/{res.pk}/')
        res.refresh_from_db()
        self.assertEqual(res.upvotes, 1)


class ThumbnailURLTest(TestCase):
    def test_thumbnail_url_format(self):
        cat = Category.objects.create(name='ThumbCat')
        res = Resource.objects.create(url='http://example.com', description='Ex', category=cat)
        expected = f'/thumbnail/{res.pk}/'
        self.assertEqual(res.thumbnail_url, expected)


class ListViewFilterSortTest(TestCase):
    def setUp(self):
        self.cat1 = Category.objects.create(name='Cat1')
        self.cat2 = Category.objects.create(name='Cat2')
        self.r1 = Resource.objects.create(url='http://1.com', description='R1', category=self.cat1, upvotes=1)
        self.r2 = Resource.objects.create(url='http://2.com', description='R2', category=self.cat2, upvotes=5)
        self.r3 = Resource.objects.create(url='http://3.com', description='R3', category=self.cat1, upvotes=2)

    def test_filter_by_category(self):
        response = self.client.get('/', {'category': self.cat1.id})
        resources = list(response.context['resources'])
        self.assertEqual(resources, [self.r3, self.r1])

    def test_sort_by_created(self):
        response = self.client.get('/', {'sort': 'created'})
        resources = list(response.context['resources'])
        self.assertEqual(resources[0], self.r3)
        self.assertEqual(resources[-1], self.r1)


class RateLimitMiddlewareTest(TestCase):
    @override_settings(
        MIDDLEWARE=settings.MIDDLEWARE + ['opensec_project.middleware.RateLimitMiddleware'],
        RATE_LIMIT_REQUESTS=2,
        RATE_LIMIT_WINDOW=60,
    )
    def test_rate_limit_blocks_excess_requests(self):
        # First two requests should pass
        self.client.get('/')
        self.client.get('/')
        # Third request should be blocked
        response = self.client.get('/')
        self.assertEqual(response.status_code, 429)


class SecurityHeadersTest(TestCase):
    @override_settings(
        SECURE_CONTENT_TYPE_NOSNIFF=True,
        SECURE_REFERRER_POLICY='same-origin',
    )
    def test_security_headers_present(self):
        response = self.client.get('/')
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(response['Referrer-Policy'], 'same-origin')


class ThumbnailErrorHandlingTest(TestCase):
    def test_thumbnail_http_error_returns_404(self):
        cat = Category.objects.create(name='ErrCat')
        res = Resource.objects.create(url='http://example.com', description='Ex', category=cat)

        with mock.patch('resources.views.urlopen', side_effect=URLError('boom')):
            response = self.client.get(f'/thumbnail/{res.pk}/')
            self.assertEqual(response.status_code, 404)


class MiddlewareConfigTest(TestCase):
    def test_invalid_rate_limit_settings_raise_error(self):
        with self.assertRaises(ValueError):
            with override_settings(RATE_LIMIT_REQUESTS='bad', RATE_LIMIT_WINDOW=60):
                RateLimitMiddleware(lambda r: r)

        with self.assertRaises(ValueError):
            with override_settings(RATE_LIMIT_REQUESTS=0, RATE_LIMIT_WINDOW=60):
                RateLimitMiddleware(lambda r: r)

