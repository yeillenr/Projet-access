from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'date_naissance', 'telephone', 'statut', 'medecin_traitant')
    list_filter = ('statut', 'sexe')
    search_fields = ('nom', 'prenom', 'telephone')
    readonly_fields = ('created_at', 'updated_at', 'annee_creation')
    fieldsets = (
        ('Identité', {'fields': ('nom', 'prenom', 'date_naissance', 'sexe')}),
        ('Coordonnées', {'fields': ('telephone', 'email', 'adresse')}),
        ('Médical', {'fields': ('groupe_sanguin', 'allergies', 'antecedents')}),
        ('Suivi', {'fields': ('statut', 'corporate', 'vivant', 'medecin_traitant')}),
        ('Audit', {'fields': ('created_at', 'updated_at', 'annee_creation')}),
    )