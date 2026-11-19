from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.consultations.statistiques import get_stats_globales


class HomeView(TemplateView):
    template_name = 'home.html'


class LoginPageView(TemplateView):
    template_name = 'login.html'


class DashboardStatsView(APIView):
    """Tableau de bord : patients reçus, chiffre d'affaires, pathologies fréquentes, taux de RDV."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_debut = request.query_params.get('date_debut')
        date_fin = request.query_params.get('date_fin')
        granularite = request.query_params.get('granularite', 'jour')
        if granularite not in ('jour', 'semaine', 'mois'):
            granularite = 'jour'
        return Response(get_stats_globales(date_debut, date_fin, granularite))
