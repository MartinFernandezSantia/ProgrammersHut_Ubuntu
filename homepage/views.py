from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    #The function returns a rendered HTML template for the homepage.
    
    return render(request, "homepage/index.html")

