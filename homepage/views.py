from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    params={}
    params["nombre_sitio"] = "ProgrammersHut"
    return render(request, "homepage/index.html", params)

