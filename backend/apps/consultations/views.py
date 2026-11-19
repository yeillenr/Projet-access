from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Avg, Count
from .models import Consultation, ParametresVitaux, Pathologie
from .serializers import ConsultationSerializer, ParametresVitauxSerializer, PathologieSerializer
from apps.users.permissions import IsAdminOrMedecin
from apps.audit.utils import AuditLogMixin, log_action


class ConsultationViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = Consultation.objects.select_related('patient', 'praticien').all()
    serializer_class = ConsultationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if not data.get('praticien'):
            from apps.users.models import Utilisateur
            user, _ = Utilisateur.objects.get_or_create(
                username='medecin_proto',
                defaults={'first_name': 'Médecin', 'last_name': 'Prototype', 'role': 'MEDECIN'}
            )
            data['praticien'] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        consultation = serializer.save()
        log_action(request, 'CREATE', Consultation._meta.db_table, consultation.pk)
        return Response(self.get_serializer(consultation).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='parametres-evolution')
    def evolution_parametres(self, request, pk=None):
        consultation = self.get_object()
        parametres = consultation.parametres.all().order_by('date_mesure')
        data = {
            'dates': [p.date_mesure.strftime('%Y-%m-%d %H:%M') for p in parametres],
            'poids': [float(p.poids) for p in parametres if p.poids],
            'tension_sys': [p.tension_sys for p in parametres if p.tension_sys],
            'tension_dia': [p.tension_dia for p in parametres if p.tension_dia],
            'imc': [p.imc for p in parametres if p.imc],
        }
        return Response(data)


class PathologieViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = Pathologie.objects.all()
    serializer_class = PathologieSerializer
    permission_classes = [IsAdminOrMedecin]
