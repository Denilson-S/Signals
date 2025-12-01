from django.urls import path
from .views import *

urlpatterns = [
    path('', list_messages, name='list_messages'),
    path('add/<int:recipient_id>/', message_create, name='add_message'),
    path('edit/<int:pk>/', message_update, name='edit_message'),
    path('delete/<int:pk>/', message_delete, name='delete_message'),
    path('detail/<int:pk>/', message_detail, name='message_detail'),
]