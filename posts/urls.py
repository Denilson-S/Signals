from django.urls import path
from .views import *

urlpatterns = [
    path('', feed_view, name='index'),
    path('create/', create_post, name='create_post'),
    path('edit/<int:pk>/', edit_post, name='edit_post'),
    path('delete/<int:pk>/', delete_post, name='delete_post'),
]