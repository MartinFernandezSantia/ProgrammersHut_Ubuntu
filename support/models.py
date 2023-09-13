from django.db import models
from datetime import datetime
from django.utils.html import format_html
from ckeditor_uploader.fields import RichTextUploadingField

class Consulta(models.Model):

    ANSWERED = "Contestada"
    NOT_ANSWERED = "No Contestada"
    IN_PROCESS = "En Proceso"

    STATUS = (
        (ANSWERED, "Contestada"),
        (NOT_ANSWERED, "No Contestada"),
        (IN_PROCESS, "En Proceso"),
    )

    nombre = models.CharField(max_length=50, blank=True, null=True)
    contenido = models.TextField(blank=False, null=False)
    estadoRespuesta = models.CharField(max_length=15, blank=True, choices=STATUS, default=NOT_ANSWERED)
    mail = models.EmailField(max_length=50, blank=True, null=True)
    fecha = models.DateField(default=datetime.now, blank=True, editable=True)

    
    def answer_status(self):
        if self.estadoRespuesta == self.ANSWERED:
            return format_html('<span style="background-color:#0a0; color: #fff; padding:5px;">{}</span>', self.estadoRespuesta, )
        elif self.estadoRespuesta == self.NOT_ANSWERED:
            return format_html('<span style="background-color:#a00; color: #fff; padding:5px;"">{}</span>', self.estadoRespuesta, )
        elif self.estadoRespuesta == self.IN_PROCESS:
            return format_html('<span style="background-color:#F0B203; color: #000; padding:5px;"">{}</span>', self.estadoRespuesta, )

class Respuesta(models.Model):

    consulta = models.ForeignKey(Consulta(), blank=True, null=True, on_delete=models.CASCADE)
    contenido = models.TextField(blank=False, null=False)
    fecha = models.DateField(default=datetime.now, blank=True, editable=True)

    def create_message(self):

        changeEstadoConsulta = Consulta.objects.get(id=self.consulta.id)
        changeEstadoConsulta.estadoRespuesta = "Contestada"
        changeEstadoConsulta.save()

    def save(self, *args, **kwargs):
        self.create_message()
        force_update = False
        if self.id:
            force_update = True
        super(Respuesta, self).save(force_update=force_update)

class PreguntasFrecuentes(models.Model):
    pregunta = models.CharField(max_length=160, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    contenido = RichTextUploadingField(blank=True, null=True)