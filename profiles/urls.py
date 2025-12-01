from django.urls import path
from .views import *

urlpatterns = [
    path('', profile_detail, name='index'),
    path('create/', profile_create, name='create_profile'),
    path('edit/<int:pk>/', profile_update, name='edit_profile'),
    path('delete/<int:pk>/', profile_delete, name='delete_profile'),
]