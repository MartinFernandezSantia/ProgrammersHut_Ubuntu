from django.urls import path

from support import views
from .admin import AdminQuery

urlpatterns = [
    path("contacto", views.Contacto.as_view(), name="contacto"),
    path("admin/contacto/consulta", AdminQuery.exportar_conversacion, name="consulta"),
    path("faq", views.preguntas_frecuentes, name="faq"),
]
