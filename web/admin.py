from django.contrib import admin
from .models import Profesor, Cliente
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('dni', 'direccion', 'genero')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('dni', 'direccion', 'genero')}),
    )
    list_display = UserAdmin.list_display + ('dni', 'direccion', 'genero')

admin.site.register(Cliente)
admin.site.register(Profesor)