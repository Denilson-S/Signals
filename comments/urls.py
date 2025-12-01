from django.urls import path
from .views import *

urlpatterns = [
    path('add/<int:post_id>/', comment_create, name='add_comment'),
    path('edit/<int:pk>/', comment_update, name='edit_comment'),
    path('delete/<int:pk>/', comment_delete, name='delete_comment'),
    path('detail/<int:pk>/', comment_detail, name='comment_detail'),
]