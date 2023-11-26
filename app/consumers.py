# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"room_{self.room_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection',
            'message': 'connected successfully',
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f'recived data: \n {json.loads(text_data)}')
        message = json.loads(text_data)
        action = message.get('action')
        time = message.get('currentTime')

        if action in ('play', 'pause'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'playback_control',
                    'data': message.get('data'),
                    'action': action,
                    'currentTime': message.get('currentTime', time)  # Receive current playback time
                }
            )

    async def playback_control(self, event):
        
        action = event['action']
        data = event['data']
        currentTime = event['currentTime']  # Get current playback time

        print(f"sent data: \n 'action': {action}, 'data': {data}, 'currentTime': {currentTime}")
        await self.send(text_data=json.dumps({
            'action': action,
            'data': data,
            'currentTime': currentTime  # Send current playback time to all users
        }))