from django import forms
from django.forms import ModelForm
from .models import Consulta
from captcha.fields import CaptchaField

# pip install django-simple-captcha
class FormQuery(ModelForm):

    captcha = CaptchaField()

    class Meta:
        # Model I'll be using in this form
        model = Consulta
        fields = [
            "nombre",
            "contenido",
            "mail",
        ]

    def send_email(self):
        # send email using the self.cleaned_data dictionary

        name = self.cleaned_data["nombre"]
        content = self.cleaned_data["contenido"]
        mail = self.cleaned_data["mail"]

        print("Enviando datos")
        print(name, content, mail)
