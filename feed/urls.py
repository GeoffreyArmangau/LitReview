from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('posts/', views.PostListView.as_view(), name='posts'),
]
