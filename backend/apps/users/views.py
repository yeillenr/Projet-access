from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Utilisateur
from .serializers import LoginSerializer, RegisterSerializer, UtilisateurSerializer
from apps.audit.utils import log_action


def _session_payload(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'nom_complet': user.nom_complet,
            'role': user.role,
        }
    }


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            log_action(request, 'LOGIN', 'users_utilisateur', user.pk, actor=user)
            return Response(_session_payload(user))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    """Création d'un compte depuis la page de connexion, puis connexion directe."""
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        log_action(request, 'CREATE', 'users_utilisateur', user.pk, details='Inscription depuis la page de connexion', actor=user)
        return Response(_session_payload(user), status=status.HTTP_201_CREATED)


class PraticienListView(ListAPIView):
    """Liste des médecins actifs (choix du praticien pour un rendez-vous)."""
    permission_classes = [IsAuthenticated]
    serializer_class = UtilisateurSerializer
    pagination_class = None
    queryset = Utilisateur.objects.filter(role='MEDECIN', is_active=True)
