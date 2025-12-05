from django.urls import path
from .views import chat_view, search_users, delete_message, edit_message

urlpatterns = [
    path('', chat_view, name='chat_index'),
    path('<int:user_id>/', chat_view, name='chat_with_user'),
    path('search/', search_users, name='search_users'),
    path('message/delete/<int:message_id>/', delete_message, name='delete_message'),
    path('message/edit/<int:message_id>/', edit_message, name='edit_message'),
]