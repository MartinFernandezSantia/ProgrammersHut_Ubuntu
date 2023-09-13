from django.contrib import sitemaps
from django.urls import reverse

class RegisterSitemap(sitemaps.Sitemap):
    priority = 0.8

    def items(self):
        return ["register",]
    
    def location(self, item):
        return reverse(item)



class LoginSitemap(sitemaps.Sitemap):
    priority = 0.8

    def items(self):
        return ["login",]
    
    def location(self, item):
        return reverse(item)