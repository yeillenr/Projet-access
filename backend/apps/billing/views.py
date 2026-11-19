from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import ActeMedical, Tarification, ConsultationActe
from .serializers import ActeMedicalSerializer, TarificationSerializer, ConsultationActeSerializer
from apps.users.permissions import IsAdmin, IsAdminOrSecretaire
from apps.audit.utils import AuditLogMixin

class ActeMedicalViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = ActeMedical.objects.all()
    serializer_class = ActeMedicalSerializer
    permission_classes = [IsAdmin]

class TarificationViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = Tarification.objects.select_related('acte').all()
    serializer_class = TarificationSerializer
    permission_classes = [IsAdmin]

class ConsultationActeViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """Association des actes médicaux à une consultation (facturation)."""
    queryset = ConsultationActe.objects.select_related('acte', 'consultation').all()
    serializer_class = ConsultationActeSerializer
    permission_classes = [IsAdminOrSecretaire]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['consultation', 'acte']