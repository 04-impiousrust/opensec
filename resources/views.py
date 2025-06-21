from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Resource, Category


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
    resource.upvotes += 1
    resource.save()
    return redirect('resource_list')
