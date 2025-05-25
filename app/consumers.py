import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from .models import Message, Room
from channels.db import database_sync_to_async
from django_redis import get_redis_connection

User = get_user_model()

def get_redis():
    return get_redis_connection("default")

def get_online_key(room_name):
    return f"online_users:{room_name}"

@database_sync_to_async
def add_user_online(room_name, user_id):
    conn = get_redis_connection("default")
    conn.sadd(get_online_key(room_name), user_id)

@database_sync_to_async
def remove_user_online(room_name, user_id):
    conn = get_redis_connection("default")
    conn.srem(get_online_key(room_name), user_id)

@database_sync_to_async
def count_users_online(room_name):
    conn = get_redis_connection("default")
    return conn.scard(get_online_key(room_name))



class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_recent_messages(self, room):
        return list(
            Message.objects
            .select_related('user', 'room')
            .filter(room=room)
            .order_by('-timestamp')[:50]
        )
    
    @database_sync_to_async
    def get_room_by_name(self, name):
        return Room.objects.get(name=name)


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Adiciona usuário à lista de online
        conn = get_redis_connection("default")
        conn.sadd(get_online_key(self.room_name), self.user.id)

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
        room = await self.get_room_by_name(self.room_name)
        recent_messages = await self.get_recent_messages(room)
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
        if self.user.is_authenticated:
            await remove_user_online(self.room_name, self.user.id)
            await self.send_online_count()


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_leave",
                "user_id": self.user.id,
            }
        )

    async def send_online_count(self):
        count = await count_users_online(self.room_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "online_count",
                "count": count
            }
        )

        await self.channel_layer.group_send(
        "lobby",
        {
            "type": "user_count_update",
            "room": self.room_name,
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
 
        elif "message" in data:
            message = data["message"]

            room = await self.get_room_by_name(self.room_name)

            await database_sync_to_async(Message.objects.create)(
                user=self.user,
                room=room,
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



class LobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("lobby", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("lobby", self.channel_name)

    async def user_count_update(self, event):
        # Envia dados para o frontend
        await self.send(text_data=json.dumps({
            'room': event['room'],
            'count': event['count'],
        }))
    
    async def new_room(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_room',
            'room': event['room'],
        }))

        