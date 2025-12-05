from django.urls import path
from .views import profile_view, edit_profile

urlpatterns = [
    path('', profile_view, name='profile'),
    path('edit/', edit_profile, name='edit_profile'),
]
