import json
from channels.generic.websocket import AsyncWebsocketConsumer


user_conections = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        if self.room_group_name not in user_conections:
            user_conections[self.room_group_name] = set()

        user_conections[self.room_group_name].add(self.user.id)
        await self.send_online_count()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if self.room_group_name in user_conections:
            user_conections[self.room_group_name].discard(self.user.id)
            await self.send_online_count()


    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if data.get('type') == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_notification',
                    'user_id': self.user.id,
                    'username': self.user.username,
                    'sender_channel': self.channel_name
                }
            )

        elif data.get('type') == 'stop_typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'stop_typing_notification',
                    'user_id': self.user.id,
                    'username': self.user.username,
                    'sender_channel': self.channel_name
                }
            )

        elif 'message' in data:
            message = data['message']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.user.username,
                    'user_id': self.user.id,
                    'image_profile': self.user.image_profile.url if self.user.image_profile else '/static/global/images/image_default.png'
                }
            )


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'image_profile': event['image_profile']
        }))

    async def typing_notification(self, event):
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'username': event['username']
            }))


    async def stop_typing_notification(self, event):
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps({
                'type': 'stop_typing',
                'username': event['username']
            }))


    async def send_online_count(self):
        total_online = len(user_conections[self.room_group_name])
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'online_count', 'count': total_online})


    async def online_count(self, event):
        await self.send(text_data=json.dumps({
            'type': 'online_count',
            'count': event['count']
        }))
