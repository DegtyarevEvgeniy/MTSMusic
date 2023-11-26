# consumers.py

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

class RoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"room_{self.room_id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        message = json.loads(text_data)
        action = message.get('action')

        if action == 'play':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'play_song',
                    'data': message.get('data')
                }
            )

    # Receive message from room group
    def play_song(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'action': 'play',
            'data': event['data']
        }))

class RoomTrackTimeConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"room_{self.room_id}_track_time"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        message = json.loads(text_data)
        action = message.get('action')

        if action == 'update_track_time':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'send_track_time',
                    'data': message.get('data')
                }
            )

    # Receive message from room group
    def send_track_time(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'action': 'update_track_time',
            'data': event['data']
        }))

