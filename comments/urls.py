from django.urls import path
from .views import add_comment, delete_comment, edit_comment

urlpatterns = [
    path('add/<int:post_id>/', add_comment, name='add_comment'),
    path('delete/<int:pk>/', delete_comment, name='delete_comment'),
    path('edit/<int:pk>/', edit_comment, name='edit_comment'),
]