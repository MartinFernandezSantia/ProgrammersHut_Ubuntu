from django.urls import path
from login import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout_request", views.logout_request, name="logout_request"),
]
