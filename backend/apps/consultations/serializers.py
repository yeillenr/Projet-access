from rest_framework import serializers
from .models import Consultation, ParametresVitaux, Pathologie, ConsultationPathologie


class ConsultationSerializer(serializers.ModelSerializer):
    montant_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    patient_nom = serializers.CharField(source='patient.nom_complet', read_only=True)

    class Meta:
        model = Consultation
        fields = ['id', 'patient', 'patient_nom', 'praticien', 'motif', 'duree_effective', 'date_consultation', 'statut_paiement', 'montant_total']

    def validate(self, data):
        if not self.partial:
            if not data.get('patient'):
                raise serializers.ValidationError({'patient': 'Le patient est obligatoire.'})
            if not data.get('motif'):
                raise serializers.ValidationError({'motif': 'Le motif est obligatoire.'})
        return data


class ParametresVitauxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametresVitaux
        fields = '__all__'


class PathologieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pathologie
        fields = '__all__'


class ConsultationPathologieSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationPathologie
        fields = '__all__'
