import json
from channels.generic.websocket import AsyncWebsocketConsumer


import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )


    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Envia a mensagem para o grupo (todos na sala)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # nome do método que será chamado
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Envia a mensagem para o WebSocket atual
        await self.send(text_data=json.dumps({
            'message': message
        }))
