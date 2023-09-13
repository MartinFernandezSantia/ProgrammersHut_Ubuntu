from django.contrib import admin
from login.models import DatosUsuario, SocialAccounts
from django.contrib.auth.models import User

###### Modificar a users en el panel admin ######
class InlineDatosUsuario(admin.TabularInline):
    model = DatosUsuario
    extra = 0

class AdminUser(admin.ModelAdmin):
    inlines = [InlineDatosUsuario]
################################################

class AdminDatosUsuario(admin.ModelAdmin):
    fieldsets = [
        ("Información del usuario", {"fields": ["user", "country"]}),
        ("Imagen de perfil", {"fields": ["avatar"]})
    ]
    list_display = ["user", "country", "check_avatar"]
    ordering = ["user"]
    # list_filter = ("user")
    search_fields = ("user__username", "country")

admin.site.register(DatosUsuario, AdminDatosUsuario)
admin.site.unregister(User)
admin.site.register(User, AdminUser)
admin.site.register(SocialAccounts)