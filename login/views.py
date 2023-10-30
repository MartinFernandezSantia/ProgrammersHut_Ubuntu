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
    """
    The function `generate_avatar` takes a seed as input and returns the content of an SVG image
    generated using the DiceBear API.

    :param seed: The seed parameter is a value that is used to generate a unique avatar. It can be any
    string or number that you choose
    :return: The function `generate_avatar` returns the content of the response if the status code is
    200 (indicating a successful request), otherwise it returns None.
    """
    url = f"https://api.dicebear.com/7.x/bottts/svg?seed={seed}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None


def is_anonymous(func):
    """
    The function `is_anonymous` is a decorator that checks if the user is anonymous and redirects them
    to the homepage if they are not.

    :param func: The `func` parameter is a function that will be wrapped by the `is_anonymous` decorator
    :return: The function `check` is being returned.
    """

    def check(*args, **kwargs):
        if not args[0].user.is_anonymous:
            messages.error(args[0], "Debe cerrar sesión para poder acceder")
            return HttpResponseRedirect("/")

        return func(*args, **kwargs)

    return check


@is_anonymous
def login(request):
    """
    The `login` function is a view function in Django that handles user authentication and login.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information about the request, such as the method used (GET or POST), the headers,
    the user's IP address, and any data sent with the request
    :return: The code is returning an HTTP response redirect to the homepage ("/") if the user is
    successfully authenticated. If the user is not authenticated, it returns an HTTP response redirect
    to the current page (request.path_info) with an error message. If the request method is not "POST",
    it renders the login.html template with the "nombre_sitio" parameter set to "Iniciar sesión".
    """
    if request.method == "POST":
        username_ = request.POST["loginUsername"]
        password_ = request.POST["loginPassword"]
        user = authenticate(request, username=username_, password=password_)

        if user is not None:
            auth_login(request, user)
            messages.success(
                request, f"¡Hola! ¡Qué bueno verte por aquí de nuevo {username_}!"
            )
            return HttpResponseRedirect("/")

        messages.error(request, "El usuario o contraseña ingresados son incorrectos")
        return HttpResponseRedirect(request.path_info)
    params = {}
    params["nombre_sitio"] = "Iniciar sesión"
    return render(request, "login/login.html", params)


@is_anonymous
def register(request):
    """
    The `register` function is used to handle user registration, validate user input, and create a new
    user account if the input is valid.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information such as the method used (GET or POST), the data sent in the request,
    and other metadata
    :return: an HTTP response. If the request method is "POST" and all the validation checks pass, it
    redirects the user to the homepage ("/") with a success message. If any of the validation checks
    fail, it redirects the user back to the registration page with an appropriate error message. If the
    request method is not "POST", it renders the registration page with the necessary parameters.
    """
    if request.method == "POST":

        username_ = request.POST.get("registerUsername")
        mail = request.POST.get("registerMail")
        password1 = request.POST.get("registerPassword1")
        password2 = request.POST.get("registerPassword2")

        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$"  # Needs upper, lower, number and at least 8
        email_pattern = r"^\S+@\S+\.\S+$"  # Needs to match email pattern
        username_pattern = "^[a-zA-Z0-9_-]{4,20}$"  # Needs to match alphanumeric, _ , and from 4 to 20 char

        if User.objects.filter(username=username_).exists() or not re.match(
            username_pattern, username_
        ):
            messages.error(
                request, f'"{username_}" ya esta en uso o no cumple los requisitos'
            )
            return HttpResponseRedirect(request.path_info)
        if User.objects.filter(email=mail).exists() or not re.match(
            email_pattern, mail
        ):
            messages.error(request, f'"{mail}" ya esta en uso o no es un mail')
            return HttpResponseRedirect(request.path_info)
        elif not re.match(password_pattern, password1):
            messages.error(
                request,
                "La contraseña ingresada es muy debil o no cumple los requisitos",
            )
            return HttpResponseRedirect(request.path_info)
        elif password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return HttpResponseRedirect(request.path_info)

        avatar_ = generate_avatar(username_)
        file_path = os.path.join(BASE_DIR, "media", "avatar", f"{username_}.svg")
        if avatar_:
            with open(file_path, "wb") as f:
                f.write(avatar_)
        user_ = User.objects.create_user(
            username=username_, email=mail, password=password1
        )
        user_data = DatosUsuario(user=user_, avatar=f"avatar/{username_}.svg").save()

        messages.success(request, "Tu cuenta ha sido exitosamente creada!!")
        return HttpResponseRedirect("/")

    params = {}
    params["nombre_sitio"] = "Crear una cuenta"
    return render(request, "login/register.html", params)


@login_required
def logout_request(request):
    """
    The function logs out the user, displays a success message, and redirects them to the homepage.

    :param request: The `request` parameter is an object that represents the current HTTP request. It
    contains information about the request, such as the user making the request, the requested URL, and
    any data sent with the request
    :return: an HttpResponseRedirect object.
    """
    logout(request)

    messages.success(request, "¡Hasta la próxima! Esperamos verte pronto.")
    return HttpResponseRedirect("/")
