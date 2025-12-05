from django.urls import path
from .views import chat_view, search_users

urlpatterns = [
    path('', chat_view, name='chat_index'),
    path('<int:user_id>/', chat_view, name='chat_with_user'),
    path('search/', search_users, name='search_users'),
]
