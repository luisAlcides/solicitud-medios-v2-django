from django.contrib import admin
from .models import Medio, Aula, Solicitud, Perfil
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    fk_name = 'user'
    verbose_name_plural = 'Perfil'
    extra = 0

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Medio)
admin.site.register(Aula)
admin.site.register(Solicitud)
admin.site.register(Perfil)
