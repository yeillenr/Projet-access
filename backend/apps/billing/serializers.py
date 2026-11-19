from rest_framework import serializers
from .models import ActeMedical, Tarification, ConsultationActe


class ActeMedicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActeMedical
        fields = '__all__'


class TarificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarification
        fields = '__all__'


class ConsultationActeSerializer(serializers.ModelSerializer):
    acte_libelle = serializers.CharField(source='acte.libelle', read_only=True)
    acte_code = serializers.CharField(source='acte.code', read_only=True)
    montant_ligne = serializers.SerializerMethodField()

    class Meta:
        model = ConsultationActe
        fields = ['id', 'consultation', 'acte', 'acte_libelle', 'acte_code', 'tarif_applique', 'quantite', 'montant_ligne', 'created_at']
        read_only_fields = ['tarif_applique', 'created_at']

    def get_montant_ligne(self, obj):
        return obj.tarif_applique * obj.quantite

    def validate(self, data):
        acte = data.get('acte') or getattr(self.instance, 'acte', None)
        consultation = data.get('consultation') or getattr(self.instance, 'consultation', None)
        if not acte or not consultation:
            raise serializers.ValidationError("L'acte et la consultation sont obligatoires.")
        tarification = Tarification.tarif_en_vigueur(acte, consultation.date_consultation.date())
        if not tarification:
            raise serializers.ValidationError(
                {'acte': f"Aucun tarif en vigueur pour « {acte.libelle} » à la date de la consultation."}
            )
        data['tarif_applique'] = tarification.montant
        return data
