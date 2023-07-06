import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    @sync_to_async
    def save_message(self, sender, room, message):
        sender_user = User.objects.get(username=sender)
        Message.objects.create(sender=sender_user, room=room, message=message)

    async def receive(self, text_data):
        # Handle received message
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user'].username
        room = self.room_name

        await self.save_message(sender, room, message)

        # Broadcast the received message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'content': message,
            'sender': sender
        }))
