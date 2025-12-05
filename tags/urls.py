from django.urls import path
from .views import dashboard_tags, create_tag, edit_tag, delete_tag

urlpatterns = [
    path('dashboard/', dashboard_tags, name='dashboard_tags'),
    path('create/', create_tag, name='create_tag'),
    path('edit/<int:pk>/', edit_tag, name='edit_tag'),
    path('delete/<int:pk>/', delete_tag, name='delete_tag'),
]
