from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from login.models import SocialAccounts
from django.contrib.auth import authenticate
from django.contrib import messages
import re
from django.http import JsonResponse
from PIL import Image
import os

@login_required
def profile(request, username):
    """
    The function retrieves user profile information and social accounts for a given username and renders
    it in a profile template.
    
    :param request: The request object represents the HTTP request that the user made to access the
    profile view. It contains information about the request, such as the user's browser, IP address, and
    any data that was sent with the request
    :param username: The username of the user whose profile is being requested
    :return: a rendered HTML template called "profiles/profile.html" with the parameters passed in the
    "params" dictionary.
    """
    params = {}
    user = User.objects.get(username=username)
    social_accounts = SocialAccounts.objects.filter(user=user)
    params["username"] = username
    params["nombre"] = user.first_name
    params["apellido"] = user.last_name
    params["email"] = user.email
    params["biography"] = user.datosusuario.biography
    params["redes_sociales"] = social_accounts
    params["pais"] = user.datosusuario.country

    if user.datosusuario.profile_pic:
        if os.path.isfile(os.path.join(user.datosusuario.profile_pic.path)):
            params["avatar"] = user.datosusuario.profile_pic
    else:
        params["avatar"] = user.datosusuario.avatar

    return render(request, "profiles/profile.html", params)

def update_profile(request, username):
    """
    The function `update_profile` updates the user's profile information, including their name, surname,
    country, biography, and password.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information about the request, such as the method used (GET or POST), the data
    sent in the request, and other metadata
    :param username: The username parameter is the username of the user whose profile is being updated
    :return: a redirect to the "index" page.
    """
    if request.method == "POST":
        name = request.POST.get("inputNombre")
        surname = request.POST.get("inputApellido")
        country = request.POST.get("inputPais")
        biography = request.POST.get("inputBio")
        curr_pass = request.POST.get("inputCurrPass")
        new_pass = request.POST.get("inputNewPass")
        new_pass2 = request.POST.get("inputNewPass2")
        check_pass = request.POST.get("checkPass", None)
        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$"
        user = User.objects.get(username=username)
        print(curr_pass,"-", new_pass,"-", new_pass2,"-",authenticate(request, username=username, password=curr_pass))


        # Update password
        if check_pass:
            if authenticate(request, username=username, password=curr_pass) is None or new_pass != new_pass2 or not re.match(password_pattern, new_pass):
                messages.error(request, "Ha ocurrido un error al intentar cambiar tu contraseña")
                return redirect("profile", username=username)
            user.set_password(new_pass)

        # Update other fields
        user.first_name = name
        user.last_name = surname
        user.datosusuario.country = country
        user.datosusuario.biography = biography
        user.save()
        user.datosusuario.save()

    messages.success(request, "Se han guardado los cambios")
    return redirect("index")


def update_avatar(request, username):
    """
    The function `update_avatar` updates the profile picture of a user with the provided image file.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), headers, and data
    :param username: The username parameter is the username of the user whose avatar is being updated
    :return: a JSON response. If the request method is 'POST' and the image file is successfully opened,
    the function returns a JSON response with the key 'success' set to True. If there is an exception or
    error, the function returns a JSON response with the key 'success' set to False.
    """
    if request.method == 'POST':
        image = request.FILES['image']
        try:
            Image.open(image)
            user = User.objects.get(username=username)
            try:
                if os.path.isfile(os.path.join(user.datosusuario.profile_pic.path)):
                    os.remove(user.datosusuario.profile_pic.path)
            except:
                pass
            user.datosusuario.profile_pic.save(f"{username}.jpg", image)
            user.datosusuario.save()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})



def add_link(request, username):
    """
    The function `add_link` adds a new link to a user's social accounts and redirects to the user's
    profile page.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information such as the HTTP method (GET, POST, etc.), headers, and any data sent
    with the request
    :param username: The username parameter is the username of the user whose profile the link is being
    added to
    :return: a redirect response to the "profile" view with the specified username as a parameter.
    """
    if request.method == "POST":
        link = request.POST.get("agregarLink")
        user = request.user
        new_link = SocialAccounts(link=link, user=user)
        new_link.save()

    messages.success(request, "Se ha agregado un link")
    return redirect("profile", username=username)

def delete_link(request, username, link_id):
    """
    The function deletes a link from a user's social accounts if the user is the owner, otherwise it
    displays an error message.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information about the request, such as the user making the request, the method
    used (GET, POST, etc.), and any data sent with the request
    :param username: The username parameter is the username of the user whose profile the link belongs
    to
    :param link_id: The `link_id` parameter is the unique identifier of the link that needs to be
    deleted. It is used to retrieve the link object from the database
    :return: a redirect response. If the link belongs to the user making the request, the function will
    delete the link, display a success message, and redirect to the profile page of the specified
    username. If the link does not belong to the user making the request, the function will display an
    error message and redirect to the profile page of the current user.
    """
    link = SocialAccounts.objects.get(id=link_id)

    if link.user == request.user:
        link.delete()
        messages.success(request, "Se ha borrado un link")
        return redirect("profile", username=username)
    
    messages.error(request, "Porfavor no intente hacer eso de nuevo. Consigase una vida")
    return redirect("profile", username=request.user.username)