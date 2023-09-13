from django.urls import path
from chat import views
#from homepage import views as home_views

urlpatterns = [
    # path("chats", home_views.index, name="chats"),
    # path("chats/<str:room_name>/", views.room, name="room"),
    path("lobby", views.room, name="lobby"),
]
