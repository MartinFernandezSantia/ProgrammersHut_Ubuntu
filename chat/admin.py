from django.contrib import admin
from chat.models import Mensajes

class AdminMensajes(admin.ModelAdmin):
    list_display = ["user", "content", "date"]
    list_filter = ("date",)

admin.site.register(Mensajes, AdminMensajes)