from django.contrib import sitemaps
from django.urls import reverse

class HomepageSitemap(sitemaps.Sitemap):
    priority = 0.9

    def items(self):
        return ["index",]
    
    def location(self, item):
        return reverse(item)