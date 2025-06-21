from django.db import models
from urllib.parse import quote


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    url = models.URLField()
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='resources')
    upvotes = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-upvotes', '-created']

    def __str__(self):
        return self.url

    @property
    def thumbnail_url(self):
        """Return the screenshot URL for the resource."""
        encoded_url = quote(self.url, safe=':/')
        # Request the screenshot with dark mode enabled so thumbnails
        # reflect how the site appears when a browser prefers a dark theme.
        return f"https://image.thum.io/get/dark/{encoded_url}"
