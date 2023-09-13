from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

# def index(request):
#     return render(request, "chat/index.html")

@login_required
def room(request): # def room(request, room_name):
    return render(request, "chat/room.html", {
        "room_name": "lobby",
        "username": request.user.username
        })
