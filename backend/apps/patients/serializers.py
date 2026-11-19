from rest_framework import serializers
from .models import Patient


class PatientListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la liste des patients (champs réduits)."""
    nom_complet = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    medecin_nom = serializers.CharField(source='medecin_traitant.nom_complet', read_only=True, default='')

    class Meta:
        model = Patient
        fields = [
            'id', 'nom', 'prenom', 'nom_complet', 'date_naissance', 'age',
            'sexe', 'telephone', 'email', 'statut', 'medecin_nom',
            'created_at', 'updated_at'
        ]


class PatientDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le détail d'un patient (tous les champs)."""
    nom_complet = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    medecin_traitant_detail = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id', 'nom', 'prenom', 'nom_complet', 'date_naissance', 'age',
            'sexe', 'telephone', 'email', 'adresse',
            'groupe_sanguin', 'allergies', 'antecedents',
            'statut', 'corporate', 'vivant', 'annee_creation',
            'medecin_traitant', 'medecin_traitant_detail',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['annee_creation', 'created_at', 'updated_at']

    def get_medecin_traitant_detail(self, obj):
        """Retourne les infos du médecin traitant."""
        if obj.medecin_traitant:
            return {
                'id': obj.medecin_traitant.id,
                'nom': obj.medecin_traitant.nom_complet,
                'email': obj.medecin_traitant.email,
                'telephone': obj.medecin_traitant.telephone,
            }
        return None

    def validate(self, data):
        """Validations personnalisées minimales et non bloquantes."""
        if data.get('medecin_traitant'):
            if data['medecin_traitant'].role != 'MEDECIN':
                raise serializers.ValidationError(
                    "Le médecin traitant doit avoir le rôle 'MEDECIN'."
                )
        if not self.partial:
            if not data.get('nom'):
                raise serializers.ValidationError({'nom': 'Le nom est obligatoire.'})
            if not data.get('prenom'):
                raise serializers.ValidationError({'prenom': 'Le prénom est obligatoire.'})
            if not data.get('date_naissance'):
                raise serializers.ValidationError({'date_naissance': 'La date de naissance est obligatoire.'})
        return data