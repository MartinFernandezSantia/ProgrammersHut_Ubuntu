from django.contrib import sitemaps
from django.urls import reverse

class ChatSitemap(sitemaps.Sitemap):
    priority = 0.8

    def items(self):
        return ["lobby",]
    
    def location(self, item):
        return reverse(item)