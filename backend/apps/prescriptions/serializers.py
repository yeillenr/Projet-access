from rest_framework import serializers
from .models import Ordonnance, LigneOrdonnance


class LigneOrdonnanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LigneOrdonnance
        fields = ['id', 'medicament', 'posologie', 'duree', 'instructions']


class OrdonnanceSerializer(serializers.ModelSerializer):
    lignes = LigneOrdonnanceSerializer(many=True, required=False)

    class Meta:
        model = Ordonnance
        fields = '__all__'

    def create(self, validated_data):
        lignes_data = validated_data.pop('lignes', [])
        ordonnance = Ordonnance.objects.create(**validated_data)
        for ligne_data in lignes_data:
            LigneOrdonnance.objects.create(ordonnance=ordonnance, **ligne_data)
        return ordonnance
