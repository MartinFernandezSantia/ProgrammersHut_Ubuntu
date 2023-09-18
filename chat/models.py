from django.db import models
from django.contrib.auth.models import User
import os

# The above class represents a model for storing messages with content, user, and date fields, and
# includes a method to retrieve the last 50 messages.
class Mensajes(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def last_50():
        return Mensajes.objects.order_by("-date").all()[:50]

# The `Imagenes` class is a model in Django that represents an image with a foreign key to a
# `Mensajes` model, and it overrides the `delete` method to also delete the associated image file.
class Imagenes(models.Model):
    id = models.BigAutoField(primary_key=True)
    img = models.ImageField(upload_to="msg_img/%Y/%m/%d/", blank=False,)
    message = models.ForeignKey(Mensajes, on_delete=models.CASCADE, blank=False)

    # Overriden method so that the image associated to the ImageField is also deleted 
    def delete(self, *args, **kwargs):
        # Delete the image file if it exists
        if self.img:
            if os.path.isfile(self.img.path):
                os.remove(self.img.path)
        # Call parent class's delete method
        super(Imagenes, self).delete(*args, **kwargs)