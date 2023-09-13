from django.contrib import admin
from .models import Respuesta, Consulta, PreguntasFrecuentes
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect

class InlineAnswer(admin.TabularInline):

    model = Respuesta
    extra = 0

class AdminQuery(admin.ModelAdmin):
    inlines = [InlineAnswer]
    list_display = ['nombre', 'contenido','mail', 'answer_status', 'fecha']
    list_filter = ['estadoRespuesta', 'fecha']
    actions = ["en_proceso", "exportar_conversacion"]

    def en_proceso(self, request, queryset):
        queryset.update(estadoRespuesta = "En Proceso")

    en_proceso.short_description = "Pasar a 'En Proceso'"

    def exportar_conversacion(self, request, queryset):
        if len(queryset) == 1:
            consultas = Consulta.objects.all().filter(mail=queryset[0].mail).order_by("fecha")
            print(consultas)
            print(queryset[0].mail)
            conversacion = []
            for i in consultas:
                try:
                    respuesta = Respuesta.objects.get(consulta=i.id)
                    res_contenido = respuesta.contenido
                    res_fecha = respuesta.fecha
                except:
                    res_contenido = res_fecha = None
                pregunta = {
                "nombre":i.nombre, 
                "mail": i.mail, 
                "fecha": i.fecha,
                "contenido": i.contenido,
                "respuesta": res_contenido,
                "fecha_respuesta": res_fecha}

                conversacion.append(pregunta)
            params= {"conversacion": conversacion}
            
            return render(request, "admin/contacto/conversacion.html", params)
        else:
            messages.error(request, "Por favor, seleccionar solo un elemento")
            return HttpResponseRedirect(request.path_info)
    exportar_conversacion.short_description = "Ver consultas y repuestas con mismo mail"
    
admin.site.register(Consulta, AdminQuery)
admin.site.register(PreguntasFrecuentes)