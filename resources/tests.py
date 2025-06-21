from django.test import TestCase
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
