import json
import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Mensajes
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = Mensajes.last_50()
        content = {
            "messages": self.messages_to_json(messages),
            "command": "fetched_messages"
        }
        self.send_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        
        return result

    def message_to_json(self, message):
        if message.date.strftime("%d/%m/%y") == datetime.date.today().strftime("%d/%m/%y"):
            date = "Hoy"
        elif message.date.strftime("%d/%m/%y") == (datetime.date.today() - datetime.timedelta(days=1)).strftime("%d/%m/%y"):
            date = "Ayer"
        else:
            date = message.date.strftime("%d/%m/%y")

        return {
            "author": message.user.username,
            "content": message.content,
            "date": date,
            "time": message.date.strftime("%I:%M %p")
        }

    def new_message(self, data):
        author = data["from"]
        user_ = User.objects.filter(username=author)[0]
        message = Mensajes.objects.create(user=user_, content=data["message"])
        content = {
            "command": "new_message",
            "message": self.message_to_json(message)
        }
        return self.send_chat_message(content)


    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message,
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self,data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))
