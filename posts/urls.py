from django.urls import path
from .views import *

urlpatterns = [
    path('', feed_view, name='index'),
    path('tag/<int:tag_id>/', tag_feed, name='tag_feed'),
    path('create/', create_post, name='create_post'),
    path('edit/<int:pk>/', edit_post, name='edit_post'),
    path('delete/<int:pk>/', delete_post, name='delete_post'),
    path('like/<int:pk>/', like_post, name='like_post'),
]