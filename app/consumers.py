import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from .models import Message
from channels.db import database_sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    # Armazena usuários online por sala
    online_users = dict()  # Ex: {'sala123': set(user_ids)}

    @database_sync_to_async
    def get_recent_messages(self):
        return list(Message.objects.select_related('user').order_by('-timestamp')[:50])

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Adiciona usuário à lista de online
        if self.room_name not in ChatConsumer.online_users:
            ChatConsumer.online_users[self.room_name] = set()
        ChatConsumer.online_users[self.room_name].add(self.user.id)

        # Envia contagem atualizada
        await self.send_online_count()

        # Notifica entrada do usuário
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_join",
                "user_id": self.user.id,
                "username": self.user.username,
                "image_profile": self.user.image_profile.url if self.user.image_profile else '/static/global/images/image_default.png'
            }
        )

        # Mensagens recentes
        recent_messages = await self.get_recent_messages()
        for msg in reversed(recent_messages):
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': msg.content,
                'username': msg.user.username,
                'user_id': msg.user.id,
                'image_profile': msg.user.image_profile.url if msg.user.image_profile else '/static/global/images/image_default.png',
                'timestamp': msg.timestamp.isoformat()
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Remove usuário da lista de online
        if self.room_name in ChatConsumer.online_users:
            ChatConsumer.online_users[self.room_name].discard(self.user.id)

        # Envia contagem atualizada
        await self.send_online_count()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_leave",
                "user_id": self.user.id,
            }
        )

    async def send_online_count(self):
        count = len(ChatConsumer.online_users.get(self.room_name, set()))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "online_count",
                "count": count
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get("type") == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing",
                    "username": self.user.username,
                    "user_id": self.user.id
                }
            )
        elif data.get("type") == "stop_typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "stop_typing",
                    "user_id": self.user.id
                }
            )
    # manter o bloco de envio de mensagem

        elif "message" in data:
            message = data["message"]

            msg = await database_sync_to_async(Message.objects.create)(
                user=self.user,
                content=message,
                timestamp=now()
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": self.user.username,
                    "user_id": self.user.id,
                    "image_profile": self.user.image_profile.url if self.user.image_profile else "/static/global/images/image_default.png"
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": event["message"],
            "username": event["username"],
            "user_id": event["user_id"],
            "image_profile": event["image_profile"]
        }))

    async def typing(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "username": event["username"],
            "user_id": event["user_id"]
        }))

    async def stop_typing(self, event):
        await self.send(text_data=json.dumps({
            "type": "stop_typing",
            "user_id": event["user_id"]
        }))

    async def user_join(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_join",
            "user_id": event["user_id"],
            "username": event["username"],
            "image_profile": event["image_profile"]
        }))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_leave",
            "user_id": event["user_id"],
        }))

    async def online_count(self, event):
        await self.send(text_data=json.dumps({
            "type": "online_count",
            "count": event["count"]
        }))
