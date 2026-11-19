from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('username', 'nom_complet', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations cabinet', {'fields': ('telephone', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations cabinet', {'fields': ('telephone', 'role')}),
    )