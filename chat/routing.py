from django.urls import re_path
import os
from . import consumers

# This code snippet is defining the URL pattern for WebSocket connections in a Django application.
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
#os.path.join("ws", "chat","")