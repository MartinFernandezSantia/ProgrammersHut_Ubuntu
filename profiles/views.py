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
    if request.method == "POST":
        name = request.POST.get("inputNombre")
        surname = request.POST.get("inputApellido")
        country = request.POST.get("inputPais")
        biography = request.POST.get("inputBio")
        # links = request.POST.getlist("inputLink")
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
    if request.method == "POST":
        link = request.POST.get("agregarLink")
        user = request.user
        new_link = SocialAccounts(link=link, user=user)
        new_link.save()

    messages.success(request, "Se ha agregado un link")
    return redirect("profile", username=username)

def delete_link(request, username, link_id):
    link = SocialAccounts.objects.get(id=link_id)

    if link.user == request.user:
        link.delete()
        messages.success(request, "Se ha borrado un link")
        return redirect("profile", username=username)
    
    messages.error(request, "Porfavor no intente hacer eso de nuevo. Consigase una vida")
    return redirect("profile", username=request.user.username)