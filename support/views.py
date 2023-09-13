from django.shortcuts import render
from .forms import FormQuery
from django.views.generic import FormView
from django.contrib import messages
from support.models import PreguntasFrecuentes



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
    params = {}
    params["preguntas"] = PreguntasFrecuentes.objects.all()

    return render(request, "support/faq.html", params)