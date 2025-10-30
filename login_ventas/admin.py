from django.contrib import admin
from django.contrib.auth.models import User
from .models import PerfilVentas

# 🔹 Inline para mostrar el perfil de ventas dentro del User
class PerfilVentasInline(admin.StackedInline):
    model = PerfilVentas
    can_delete = False
    verbose_name_plural = 'Perfil Ventas'

# 🔹 Custom UserAdmin para que se pueda crear el perfil de ventas desde el mismo User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilVentasInline,)

# 🔹 Desregistrar el User original y registrar el nuevo con inline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# 🔹 Registrar también PerfilVentas de forma independiente por si querés verlo directo
class PerfilVentasAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo')
    search_fields = ('user__username',)
    list_filter = ('tipo',)

admin.site.register(PerfilVentas, PerfilVentasAdmin)