import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        
        if self.user.is_anonymous:
            await self.close()
            return

        # Create a room name based on both user IDs (sorted to be unique for the pair)
        users = sorted([int(self.user.id), int(self.other_user_id)])
        self.room_group_name = f'chat_{users[0]}_{users[1]}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_id = self.other_user_id

        # Save message to database and get needed data safely
        message_data = await self.save_message(self.user.id, receiver_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id,
                'timestamp': message_data['timestamp'],
                'sender_avatar': message_data['sender_avatar']
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        timestamp = event['timestamp']
        sender_avatar = event.get('sender_avatar')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'timestamp': timestamp,
            'sender_avatar': sender_avatar
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        msg = Message.objects.create(sender=sender, receiver=receiver, content=content)
        
        # Access related fields synchronously to avoid async errors
        avatar_url = None
        if hasattr(sender, 'profile') and sender.profile.avatar:
            avatar_url = sender.profile.avatar.url
            
        return {
            'timestamp': msg.timestamp.strftime('%I:%M %p'),
            'sender_avatar': avatar_url
        }