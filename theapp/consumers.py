# theapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class GlobalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "global_room"
        print("GLOBAL CONNECT:", self.channel_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("GLOBAL RECEIVE RAW:", text_data)
        data = json.loads(text_data)
        message = data.get("message")
        username = data.get("username", "guest")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            }
        )

    async def chat_message(self, event):
        print("GLOBAL GROUP EVENT:", event)
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
        }))


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"private_{self.room_name}"
        print("PRIVATE CONNECT:", self.channel_name, "group =", self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("PRIVATE RECEIVE RAW:", text_data)
        data = json.loads(text_data)
        message = data.get("message")
        username = data.get("username", "guest")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            }
        )

    async def chat_message(self, event):
        print("PRIVATE GROUP EVENT:", event)
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
        }))
