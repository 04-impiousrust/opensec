from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from .models import Resource, Category
import io
from urllib.request import urlopen


class ResourceListView(ListView):
    model = Resource
    template_name = 'resources/list.html'
    context_object_name = 'resources'


class ResourceCreateView(CreateView):
    model = Resource
    fields = ['url', 'description', 'category']
    template_name = 'resources/create.html'
    success_url = reverse_lazy('resource_list')


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'resources/category_create.html'
    success_url = reverse_lazy('resource_list')


def upvote(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    upvoted = request.session.get('upvoted_resources', [])
    if pk not in upvoted:
        resource.upvotes += 1
        resource.save()
        upvoted.append(pk)
        request.session['upvoted_resources'] = upvoted
    return redirect('resource_list')


def thumbnail(request, pk):
    """Return an inverted thumbnail screenshot for the resource."""
    resource = get_object_or_404(Resource, pk=pk)
    screenshot_url = f"https://image.thum.io/get/{resource.url}"
    try:
        with urlopen(screenshot_url) as response:
            image_bytes = response.read()
    except Exception as exc:
        raise Http404 from exc

    try:
        from PIL import Image, ImageOps  # type: ignore
    except Exception:
        return HttpResponse(image_bytes, content_type="image/png")

    try:
        img = Image.open(io.BytesIO(image_bytes))
        inverted = ImageOps.invert(img.convert("RGB"))
        buffer = io.BytesIO()
        inverted.save(buffer, format="PNG")
        return HttpResponse(buffer.getvalue(), content_type="image/png")
    except Exception as exc:
        raise Http404 from exc
