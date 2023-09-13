from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

class DatosUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, db_index=True, blank=False, null=True, on_delete=models.CASCADE)    
    country = models.CharField(max_length=30, blank=True)
    avatar = models.CharField(max_length=300, default="media/defaultAvatar.svg")
    biography = models.TextField(null=True, blank=True, default="")
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profile_pics/")
    

    def check_avatar(self):
        if self.avatar == "media/avatars/default_avatar.svg":
            return format_html("<span style='background-color:#ffc107'>{}</span>", self.avatar,)
        else:
            return self.avatar
        
    def get_absolute_url(self):
        return f"/profile/{self.user.username}"

@receiver(pre_delete, sender=DatosUsuario)
def delete_datosusuario_images(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(os.path.join("media", instance.avatar)):
            os.remove(os.path.join("media", instance.avatar))
    if instance.profile_pic:
        if os.path.isfile(instance.profile_pic.path):
            os.remove(instance.profile_pic.path)

    def __str__(self):
        return self.user.username


class SocialAccounts(models.Model):
     id = models.AutoField(primary_key=True)
     link = models.CharField(max_length=300, null=False)
     user = models.ForeignKey(User, on_delete=models.CASCADE)