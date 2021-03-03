import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model, models
from asgiref.sync import sync_to_async

User = get_user_model()

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

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        message = data['message']
        sender = data['sender']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender,
                'message': message
            }
        )
        await self.save_message(
            {
                'sender': sender,
                'message': message
            }
        )
       

    async def chat_message(self, event):
        print("chat_message")
        message = event['message']
        sender = event['sender']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
            
        }))
        await self.fetch_message(self) 


    async def send_message(self, message):
        print("send message")
        self.send(text_data=json.dumps(message))
    
    @database_sync_to_async
    def save_message(self, data):
        print("save message")
        author = data['sender']
        author_user = User.objects.filter(username=author)[0]
        Message.objects.create(
            author=author_user,
            content=data['message']
        )

    @database_sync_to_async    
    def fetch_message(self, data):
        messages = Message.last_10_messages(self)
        for message in messages:
            print("enviando...", message.content)
            self.send({
                'message': message.content,
                'sender': message.author,
                'ts': message.timestamp
            })

        



