from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.patients.views import PatientViewSet
from apps.appointments.views import RendezVousViewSet
from apps.consultations.views import ConsultationViewSet, PathologieViewSet
from apps.billing.views import ActeMedicalViewSet, TarificationViewSet, ConsultationActeViewSet
from apps.prescriptions.views import OrdonnanceViewSet
from apps.reports.views import rapportViewSet
from apps.core.views import DashboardStatsView

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'rdv', RendezVousViewSet, basename='rendezvous')
router.register(r'consultations', ConsultationViewSet, basename='consultation')
router.register(r'pathologies', PathologieViewSet, basename='pathologie')
router.register(r'actes', ActeMedicalViewSet, basename='actemedical')
router.register(r'tarifs', TarificationViewSet, basename='tarification')
router.register(r'consultation-actes', ConsultationActeViewSet, basename='consultationacte')
router.register(r'ordonnances', OrdonnanceViewSet, basename='ordonnance')
router.register(r'comptes-rendus', rapportViewSet, basename='compterendu')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('apps.users.urls')),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]