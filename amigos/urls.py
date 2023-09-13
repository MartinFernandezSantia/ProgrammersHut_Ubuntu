from django.urls import path
from .views import BuscarAmigo
urlpatterns = [
    path("buscar_usuario/", BuscarAmigo.as_view(), name="buscar_usuario"),
]
