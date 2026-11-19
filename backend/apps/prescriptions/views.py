from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import get_template
from django_filters.rest_framework import DjangoFilterBackend
from xhtml2pdf import pisa
from .models import Ordonnance
from .serializers import OrdonnanceSerializer
from apps.users.permissions import IsAdminOrMedecin
from apps.audit.utils import AuditLogMixin

class OrdonnanceViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = Ordonnance.objects.select_related('patient', 'consultation').prefetch_related('lignes').all()
    serializer_class = OrdonnanceSerializer
    permission_classes = [IsAdminOrMedecin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['consultation', 'patient']

    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        ordonnance = self.get_object()
        context = {'ordonnance': ordonnance}
        template = get_template('ordonnance_pdf.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=ordonnance_{ordonnance.id}.pdf'
        result = pisa.CreatePDF(html, dest=response)
        if result.err:
            return Response({'detail': 'Erreur lors de la génération du PDF.'}, status=500)
        return response