from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import get_template
from django_filters.rest_framework import DjangoFilterBackend
from xhtml2pdf import pisa
from .models import CompteRendu
from .serializers import rapportSerializer
from apps.users.permissions import IsAdminOrMedecin
from apps.audit.utils import AuditLogMixin


class rapportViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = CompteRendu.objects.select_related('patient', 'consultation').all()
    serializer_class = rapportSerializer
    permission_classes = [IsAdminOrMedecin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['consultation', 'patient']

    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        rapport = self.get_object()
        context = {'rapport': rapport}
        template = get_template('rapport_pdf.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=rapport_{rapport.id}.pdf'
        result = pisa.CreatePDF(html, dest=response)
        if result.err:
            return Response({'detail': 'Erreur lors de la génération du PDF.'}, status=500)
        return response