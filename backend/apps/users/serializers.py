from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    nom_complet = serializers.CharField(read_only=True)

    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'nom_complet', 'role', 'telephone', 'is_active', 'date_creation']
        read_only_fields = ['date_creation']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Identifiants invalides.")

class RegisterSerializer(serializers.Serializer):
    """Création de compte depuis la page de connexion (rôle administrateur exclu)."""
    ROLES_AUTORISES = (('MEDECIN', 'Médecin'), ('SECRETAIRE', 'Secrétaire'))

    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=ROLES_AUTORISES)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if Utilisateur.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Cet identifiant est déjà utilisé.")
        return value

    def validate(self, data):
        user = Utilisateur(username=data['username'], first_name=data['first_name'],
                           last_name=data['last_name'], email=data.get('email', ''))
        try:
            validate_password(data['password'], user)
        except Exception as exc:
            raise serializers.ValidationError({'password': list(exc.messages)})
        return data

    def create(self, validated_data):
        return Utilisateur.objects.create_user(**validated_data)
