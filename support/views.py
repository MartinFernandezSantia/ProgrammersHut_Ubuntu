from django.shortcuts import render
from .forms import FormQuery
from django.views.generic import FormView
from django.contrib import messages
from support.models import PreguntasFrecuentes



# The Contacto class is a FormView that handles form submission, saves the form data, sends an email,
# and redirects to a success URL.
class Contacto(FormView):

    template_name = "support/contacto.html"
    form_class = FormQuery
    success_url = "/"

    def form_valid(self, form):
        # Si el formulario es valido, hace esto:
        # 1) Llama al método save() que se encuentra dentro del formulario
        # 2) Redirecciona
        form.save()
        messages.success(self.request,"Gracias por su consulta. Nos pondremos en contacto con usted lo antes posible.")
        form.send_email()
        return super().form_valid(form)
    
def preguntas_frecuentes(request):
    """
    The function "preguntas_frecuentes" retrieves all the frequently asked questions from the database
    and renders them in the "faq.html" template.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    user. It contains information such as the user's browser, IP address, and any data sent with the
    request
    :return: a rendered HTML template called "faq.html" with a context variable "params" that contains
    all the objects from the "PreguntasFrecuentes" model.
    """
    params = {}
    params["preguntas"] = PreguntasFrecuentes.objects.all()

    return render(request, "support/faq.html", params)