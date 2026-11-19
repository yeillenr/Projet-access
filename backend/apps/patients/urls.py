from rest_framework import serializers
from .models import Patient

class PatientListSerializer(serializers.ModelSerializer):
    nom_complet = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    medecin_nom = serializers.CharField(source='medecin_traitant.nom_complet', read_only=True, default='')

    class Meta:
        model = Patient
        fields = ['id', 'nom', 'prenom', 'nom_complet', 'date_naissance', 'age', 'sexe', 'telephone', 'email', 'statut', 'medecin_nom', 'created_at']

class PatientDetailSerializer(serializers.ModelSerializer):
    nom_complet = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'annee_creation']