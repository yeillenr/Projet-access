from rest_framework import serializers
from .models import CompteRendu


class rapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompteRendu
        fields = '__all__'
