from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import RendezVous
from .serializers import RendezVousSerializer
from apps.users.permissions import IsAdminOrSecretaire
from apps.audit.utils import AuditLogMixin

class RendezVousViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = RendezVous.objects.select_related('patient', 'praticien').all()
    serializer_class = RendezVousSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['patient', 'praticien', 'statut', 'date_heure']
    ordering_fields = ['date_heure']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminOrSecretaire]
        else:
            # Lecture du calendrier : accessible à tout le personnel connecté
            # (secrétariat, médecin, admin), pas seulement à ceux qui écrivent.
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()