from django.db import models
from django.urls import reverse


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
        """Return the URL of the generated thumbnail."""
        return reverse("resource_thumbnail", args=[self.pk])
