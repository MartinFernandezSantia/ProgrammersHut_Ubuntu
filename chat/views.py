from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def room(request): # def room(request, room_name):
    """
    The function "room" renders the "room.html" template with the room name set to "lobby" and the
    username set to the username of the current user.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information about the request, such as the user making the request, the HTTP
    method used (GET, POST, etc.), and any data sent with the request
    :return: a rendered HTML template called "room.html" with the context variables "room_name" and
    "username". The value of "room_name" is set to "lobby" and the value of "username" is set to the
    username of the user making the request.
    """
    return render(request, "chat/room.html", {
        "room_name": "lobby",
        "username": request.user.username
        })
