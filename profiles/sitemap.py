from django.contrib import sitemaps
from login.models import DatosUsuario

class ProfilesSitemap(sitemaps.Sitemap):
    priority = 0.7

    def items(self):
        return DatosUsuario.objects.all()