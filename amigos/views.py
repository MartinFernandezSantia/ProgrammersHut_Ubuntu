from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import View
from django.http import HttpResponse
import json
import mimetypes
from http.client import HTTPResponse
import os

# The `BuscarAmigo` class is a view in a Python Django application that handles an AJAX request to
# search for users based on a given term and returns the results in JSON format.
class BuscarAmigo(View):

    def get(self, request):
        if request.is_ajax:
            palabra=request.GET.get('term', '')
            print(palabra)
            users=User.objects.filter(username__icontains=palabra)
            result=[]
            for user in users:
                data={}
                data['label']=user.username # If using standard autocomplete, the key must be "label"
                if user.datosusuario.profile_pic:
                    if os.path.isfile(os.path.join(user.datosusuario.profile_pic.path)):
                        data["avatar"] = os.path.join("profile_pics", user.username + ".jpg") # Doing it like this 'cause ImageField isn't working with json
                else:
                    data["avatar"] = user.datosusuario.avatar
                data["username"] = user.username
                result.append(data)
            data_json=json.dumps(result)
        else:
            data_json="fallo"
        mimetype="application/json"
        return HttpResponse(data_json, mimetype)