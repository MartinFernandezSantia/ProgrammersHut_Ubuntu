from django.contrib import sitemaps
from django.urls import reverse

class ContactoSitemap(sitemaps.Sitemap):
    priority = 0.7

    def items(self):
        return ["contacto",]
    
    def location(self, item):
        return reverse(item)