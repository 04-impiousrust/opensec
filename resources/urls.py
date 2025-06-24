from django.urls import path
from . import views

urlpatterns = [
    path('', views.ResourceListView.as_view(), name='resource_list'),
    path('add/', views.ResourceCreateView.as_view(), name='resource_add'),
    path("manage/", views.ResourceAdminListView.as_view(), name="admin_resource_list"),
    path("manage/add/", views.ResourceAdminCreateView.as_view(), name="admin_resource_add"),
    path("manage/<int:pk>/edit/", views.ResourceAdminUpdateView.as_view(), name="admin_resource_edit"),
    path("manage/<int:pk>/delete/", views.ResourceAdminDeleteView.as_view(), name="admin_resource_delete"),
    path('category/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('upvote/<int:pk>/', views.upvote, name='resource_upvote'),
    path('thumbnail/<int:pk>/', views.thumbnail, name='resource_thumbnail'),
]
