from django.shortcuts import render
from login.models import DatosUsuario
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File
# from django.conf import settings
import re
import requests
import os
# Create your views here.

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def generate_avatar(seed):
    url = f"https://avatars.dicebear.com/api/bottts/{seed}.svg"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

# Decorator to check if user is anonymous
def is_anonymous(func):
    def check(*args, **kwargs):
        if not args[0].user.is_anonymous:
            messages.error(args[0],"Debe cerrar sesión para poder acceder")
            return HttpResponseRedirect("/") 
        
        return func(*args, **kwargs)
    return check

@is_anonymous
def login(request):
    if request.method == "POST":
        username_ = request.POST["loginUsername"]
        password_ = request.POST["loginPassword"]
        user = authenticate(request, username=username_, password=password_)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f"¡Hola! ¡Qué bueno verte por aquí de nuevo {username_}!")
            return HttpResponseRedirect('/')

        messages.error(request, "El usuario o contraseña ingresados son incorrectos")
        return HttpResponseRedirect(request.path_info)
    params = {}
    params["nombre_sitio"] = "Iniciar sesión"
    return render(request, "login/login.html", params)


@is_anonymous
def register(request):
    if request.method == "POST":

        username_ = request.POST.get("registerUsername")
        mail = request.POST.get("registerMail")
        password1 = request.POST.get("registerPassword1")
        password2 = request.POST.get("registerPassword2")

        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$" # Needs upper, lower, number and at least 8
        email_pattern = r"^\S+@\S+\.\S+$" # Needs to match email pattern
        username_pattern = "^[a-zA-Z0-9_-]{4,20}$" # Needs to match alphanumeric, _ , and from 4 to 20 char

        if User.objects.filter(username=username_).exists() or not re.match(username_pattern, username_):
            messages.error(request, f'"{username_}" ya esta en uso o no cumple los requisitos')
            return HttpResponseRedirect(request.path_info)

        if User.objects.filter(email = mail).exists() or not re.match(email_pattern, mail):
            messages.error(request, f'"{mail}" ya esta en uso o no es un mail')
            return HttpResponseRedirect(request.path_info)
        elif not re.match(password_pattern, password1):
            messages.error(request, "La contraseña ingresada es muy debil o no cumple los requisitos")
            return HttpResponseRedirect(request.path_info)
        elif password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return HttpResponseRedirect(request.path_info)

        

        avatar_ = generate_avatar(username_)
        file_path = os.path.join(BASE_DIR, "media", "avatar", f"{username_}.svg")
        if avatar_:
            with open(file_path, "wb") as f:
                f.write(avatar_)
        user_ = User.objects.create_user(username=username_, email=mail, password=password1)
        user_data = DatosUsuario(user=user_, avatar=f"avatar/{username_}.svg").save()


        messages.success(request,"Tu cuenta ha sido exitosamente creada!!")
        return HttpResponseRedirect('/')

    params = {}
    params["nombre_sitio"] = "Crear una cuenta"
    return render(request, "login/register.html", params)

@login_required
def logout_request(request):
    logout(request)

    messages.success(request,"¡Hasta la próxima! Esperamos verte pronto.")
    return HttpResponseRedirect('/')
