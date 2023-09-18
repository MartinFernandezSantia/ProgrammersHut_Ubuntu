import json
import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Mensajes
from django.contrib.auth.models import User

# The `ChatConsumer` class is a WebSocket consumer that handles fetching and sending chat messages in
# a chat room.
class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        """
        The function fetches the last 50 messages and sends them as JSON data along with a command to
        the recipient.
        
        :param data: The parameter `data` is not used in the `fetch_messages` method. It is likely that
        it was intended to be used for some additional functionality, but it is not currently being used
        in the provided code
        """
        messages = Mensajes.last_50()
        content = {
            "messages": self.messages_to_json(messages),
            "command": "fetched_messages"
        }
        self.send_message(content)

    def messages_to_json(self, messages):
        """
        The function "messages_to_json" converts a list of messages into a JSON format.
        
        :param messages: The "messages" parameter is a list of message objects
        :return: a list of JSON objects.
        """
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        
        return result

    def message_to_json(self, message):
        """
        The function converts a message object into a JSON format with author, content, date, and time
        attributes.
        
        :param message: The `message` parameter is an object that represents a message. It likely has
        properties such as `date`, `user`, and `content`
        :return: a dictionary with the following keys and values:
        - "author": the username of the message's user
        - "content": the content of the message
        - "date": the date of the message in the format "dd/mm/yy" (if the message was sent today, it
        will be "Hoy"; if it was sent yesterday, it will be "Ayer"
        """
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
        """
        The function creates a new message object and sends it as a chat message.
        
        :param data: The `data` parameter is a dictionary that contains the following keys:
        :return: the result of calling the `send_chat_message` method with the `content` parameter.
        """
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
        """
        The function connects a user to a chat room by adding them to a group and accepting the
        connection.
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        """
        The `disconnect` function removes the current channel from the specified room group.
        
        :param close_code: The `close_code` parameter is an integer that represents the reason for
        disconnecting. It is typically used in WebSocket connections to indicate the reason for closing
        the connection
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        """
        The function receives text data, parses it as JSON, and calls the appropriate command based on
        the "command" key in the data.
        
        :param text_data: The `text_data` parameter is a string that contains the data received from the
        client
        """
        data = json.loads(text_data)
        self.commands[data["command"]](self,data)

    def send_chat_message(self, message):
        """
        The function sends a chat message to a group using the channel layer.
        
        :param message: The "message" parameter is the content of the chat message that you want to
        send. It can be a string or any other data type that represents the message you want to send
        """
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def send_message(self, message):
        """
        The function sends a message by converting it to JSON format and then sending it.
        
        :param message: The `message` parameter is the data that you want to send as a message. It can
        be any type of data, such as a string, dictionary, or list. The `send_message` method takes this
        `message` and sends it to the recipient
        """
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        """
        The function sends a chat message by converting it to JSON and sending it as text data.
        
        :param event: The `event` parameter is a dictionary that contains information about the chat
        message event. It typically includes details such as the sender of the message, the content of
        the message, and any other relevant information
        """
        message = event["message"]
        self.send(text_data=json.dumps(message))

