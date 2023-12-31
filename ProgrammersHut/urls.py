from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from homepage import views
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from chat.sitemap import ChatSitemap
from support.sitemap import ContactoSitemap
from homepage.sitemap import HomepageSitemap
from login.sitemap import RegisterSitemap, LoginSitemap
from profiles.sitemap import ProfilesSitemap


sitemaps = {
    "chat": ChatSitemap,
    "contacto": ContactoSitemap,
    "index": HomepageSitemap,
    "register": RegisterSitemap,
    "login": LoginSitemap,
    "profiles": ProfilesSitemap,
}

urlpatterns = [
    path("accounts/", include("registration.backends.default.urls")),
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("", include("login.urls")),
    path("", views.index, name="index"),
    path("", include("chat.urls")),
    path("captcha/", include("captcha.urls")),
    path("", include("support.urls")),
    path("", include("amigos.urls")),
    path("", include("profiles.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("", include('ckeditor_uploader.urls'))
]

if settings.DEBUG:
    #import debug_toolbar

    #urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

