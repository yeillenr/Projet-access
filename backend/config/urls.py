from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from apps.core.views import HomeView, LoginPageView
from django.views.generic import TemplateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginPageView.as_view(), name='login-page'),
    path('patients/', TemplateView.as_view(template_name='patients.html'), name='patients-page'),
    path('patients/<int:pk>/', TemplateView.as_view(template_name='dossier_patient.html'), name='patient-dossier'),
    path('consultations/', TemplateView.as_view(template_name='consultations.html'), name='consultations-page'),
    path('appointments/', TemplateView.as_view(template_name='appointments.html'), name='appointments-page'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]