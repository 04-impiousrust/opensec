from django.urls import path
from . import views

urlpatterns = [
    path('', views.ResourceListView.as_view(), name='resource_list'),
    path('add/', views.ResourceCreateView.as_view(), name='resource_add'),
    path('category/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('upvote/<int:pk>/', views.upvote, name='resource_upvote'),
    path('thumbnail/<int:pk>/', views.thumbnail, name='resource_thumbnail'),
]
