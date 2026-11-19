from django.db.models import Count, Sum, F
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth

from apps.patients.models import Patient
from apps.appointments.models import RendezVous
from apps.billing.models import ConsultationActe
from .models import Consultation, ConsultationPathologie

TRUNC_FUNCS = {'jour': TruncDate, 'semaine': TruncWeek, 'mois': TruncMonth}


def _borne_dates(qs, champ, date_debut=None, date_fin=None):
    if date_debut:
        qs = qs.filter(**{f'{champ}__date__gte': date_debut})
    if date_fin:
        qs = qs.filter(**{f'{champ}__date__lte': date_fin})
    return qs


def patients_par_periode(granularite='jour', date_debut=None, date_fin=None):
    """Nombre de patients distincts reçus, groupés par période et par praticien."""
    trunc = TRUNC_FUNCS.get(granularite, TruncDate)
    qs = _borne_dates(Consultation.objects.all(), 'date_consultation', date_debut, date_fin)
    return list(
        qs.annotate(periode=trunc('date_consultation'))
          .values('periode', 'praticien__id', 'praticien__first_name', 'praticien__last_name')
          .annotate(nb_patients=Count('patient', distinct=True))
          .order_by('periode')
    )


def chiffre_affaires(date_debut=None, date_fin=None):
    """CA total, réparti par acte médical et par praticien, sur une période donnée."""
    qs = ConsultationActe.objects.select_related('consultation', 'acte')
    qs = _borne_dates(qs, 'consultation__date_consultation', date_debut, date_fin)
    montant_expr = F('tarif_applique') * F('quantite')

    total = qs.aggregate(total=Sum(montant_expr))['total'] or 0

    par_acte = list(
        qs.values('acte__id', 'acte__libelle')
          .annotate(montant=Sum(montant_expr))
          .order_by('-montant')
    )

    par_praticien = list(
        qs.values(
            'consultation__praticien__id',
            'consultation__praticien__first_name',
            'consultation__praticien__last_name',
        )
        .annotate(montant=Sum(montant_expr))
        .order_by('-montant')
    )

    return {'total': total, 'par_acte': par_acte, 'par_praticien': par_praticien}


def pathologies_frequentes(limite=10):
    """Pathologies les plus fréquemment diagnostiquées (suivi épidémiologique simple)."""
    return list(
        ConsultationPathologie.objects
        .values('pathologie__id', 'pathologie__libelle', 'pathologie__code_cim10')
        .annotate(nb=Count('id'))
        .order_by('-nb')[:limite]
    )


def taux_rendez_vous(date_debut=None, date_fin=None):
    """Taux de rendez-vous honorés / annulés / absents sur une période donnée."""
    qs = _borne_dates(RendezVous.objects.all(), 'date_heure', date_debut, date_fin)
    total = qs.count()
    if total == 0:
        return {'total': 0, 'honores': 0, 'annules': 0, 'absents': 0,
                'taux_honores': 0, 'taux_annules': 0, 'taux_absents': 0}

    honores = qs.filter(statut='TERMINE').count()
    annules = qs.filter(statut='ANNULE').count()
    absents = qs.filter(statut='ABSENT').count()
    return {
        'total': total, 'honores': honores, 'annules': annules, 'absents': absents,
        'taux_honores': round(honores / total * 100, 1),
        'taux_annules': round(annules / total * 100, 1),
        'taux_absents': round(absents / total * 100, 1),
    }


def get_stats_globales(date_debut=None, date_fin=None, granularite='jour'):
    consultations_qs = _borne_dates(Consultation.objects.all(), 'date_consultation', date_debut, date_fin)
    return {
        'patients_actifs': Patient.objects.filter(statut='ACTIF').count(),
        'consultations_periode': consultations_qs.count(),
        'patients_par_periode': patients_par_periode(granularite, date_debut, date_fin),
        'chiffre_affaires': chiffre_affaires(date_debut, date_fin),
        'rendez_vous': taux_rendez_vous(date_debut, date_fin),
        'pathologies_frequentes': pathologies_frequentes(),
    }
