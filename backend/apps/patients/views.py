import os
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.core.files.base import ContentFile

from .models import Patient
from .serializers import PatientListSerializer, PatientDetailSerializer
from .import_excel import importer_patients_excel
from apps.audit.utils import AuditLogMixin, log_action
from apps.users.permissions import IsAdminOrMedecin
from apps.consultations.models import Consultation
from apps.consultations.serializers import ConsultationSerializer, ParametresVitauxSerializer
from apps.prescriptions.models import Ordonnance
from apps.prescriptions.serializers import OrdonnanceSerializer
from apps.reports.models import CompteRendu
from apps.reports.serializers import rapportSerializer
from apps.billing.models import ConsultationActe
from apps.billing.serializers import ConsultationActeSerializer


class PatientViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des patients.
    Permet les opérations CRUD + recherche avancée.
    """
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'sexe', 'corporate', 'vivant']
    search_fields = ['nom', 'prenom', 'telephone', 'email']
    ordering_fields = ['nom', 'prenom', 'date_naissance', 'date_creation']
    ordering = ['nom', 'prenom']

    def get_queryset(self):
        """Retourne la liste des patients (avec optimisation)."""
        return Patient.objects.select_related('medecin_traitant').all()

    def get_serializer_class(self):
        """Utilise un sérialiseur différent pour la liste et le détail."""
        if self.action == 'list':
            return PatientListSerializer
        return PatientDetailSerializer

    def get_permissions(self):
        if self.action == 'dossier':
            # Regroupe des données médicales sensibles (ordonnances, comptes rendus) :
            # réservé au personnel soignant, contrairement au reste du ViewSet (AllowAny).
            self.permission_classes = [IsAdminOrMedecin]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()
        log_action(request, 'CREATE', Patient._meta.db_table, patient.pk)
        response_serializer = PatientListSerializer(patient)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """
        Recherche avancée des patients.
        Paramètres acceptés : q (texte libre), statut, sexe, etc.
        """
        queryset = self.get_queryset()
        query = request.query_params.get('q', '')

        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) |
                Q(prenom__icontains=query) |
                Q(telephone__icontains=query) |
                Q(email__icontains=query)
            )

        # Filtres supplémentaires
        statut = request.query_params.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)

        sexe = request.query_params.get('sexe')
        if sexe:
            queryset = queryset.filter(sexe=sexe)

        # Pagination manuelle
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PatientListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PatientListSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        """Désactivation du patient plutôt que suppression définitive."""
        instance.statut = 'INACTIF'
        instance.save()
        log_action(self.request, 'UPDATE', Patient._meta.db_table, instance.pk, details='Désactivation du patient')

    @action(detail=True, methods=['post'])
    def reactiver(self, request, pk=None):
        """Réactiver un patient inactif."""
        patient = self.get_object()
        if patient.statut == Patient.Statut.ACTIF:
            return Response(
                {'detail': 'Le patient est déjà actif.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        patient.statut = 'ACTIF'
        patient.save()
        log_action(request, 'UPDATE', Patient._meta.db_table, patient.pk, details='Réactivation du patient')
        return Response(
            {'detail': 'Patient réactivé avec succès.'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def dossier(self, request, pk=None):
        """
        Fiche patient unique : identité + historique complet regroupé par consultation
        (constantes, ordonnance, compte rendu, actes facturés). Cf. cahier des charges §5.1.
        """
        patient = self.get_object()

        consultations = Consultation.objects.filter(patient=patient).select_related('praticien').prefetch_related(
            'parametres', 'diagnostics__pathologie'
        ).order_by('-date_consultation')

        ordonnances = {o.consultation_id: o for o in Ordonnance.objects.filter(patient=patient).prefetch_related('lignes')}
        comptes_rendus = {c.consultation_id: c for c in CompteRendu.objects.filter(patient=patient)}
        actes_par_consultation = {}
        for ca in ConsultationActe.objects.filter(consultation__patient=patient).select_related('acte', 'consultation'):
            actes_par_consultation.setdefault(ca.consultation_id, []).append(ca)

        historique = []
        for c in consultations:
            ordonnance = ordonnances.get(c.id)
            compte_rendu = comptes_rendus.get(c.id)
            actes = actes_par_consultation.get(c.id, [])
            historique.append({
                'consultation': ConsultationSerializer(c).data,
                'parametres_vitaux': ParametresVitauxSerializer(c.parametres.all(), many=True).data,
                'ordonnance': OrdonnanceSerializer(ordonnance).data if ordonnance else None,
                'compte_rendu': rapportSerializer(compte_rendu).data if compte_rendu else None,
                'actes_factures': ConsultationActeSerializer(actes, many=True).data,
            })

        return Response({
            'patient': PatientDetailSerializer(patient).data,
            'historique': historique,
        })

    @action(detail=False, methods=['post'], url_path='import-excel')
    def import_excel(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'detail': 'Aucun fichier fourni.'}, status=400)

        temp_path = None
        try:
            content = file_obj.read()
            temp_path = os.path.join('/tmp', file_obj.name)
            with open(temp_path, 'wb') as handle:
                handle.write(content)
            result = importer_patients_excel(temp_path, request.user)
            return Response(result)
        except Exception as exc:
            return Response({'detail': str(exc)}, status=500)
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
