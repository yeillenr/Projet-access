import openpyxl
from django.db import transaction
from .models import Patient

def importer_patients_excel(fichier, utilisateur):
    wb = openpyxl.load_workbook(fichier)
    sheet = wb.active
    resultats = {'total': 0, 'importes': 0, 'erreurs': []}

    for row in sheet.iter_rows(min_row=2, values_only=True):
        # Mapping personnalisé
        nom, prenom, date_naissance, sexe, telephone, email, adresse = row[:7]
        if not nom or not prenom:
            continue

        try:
            with transaction.atomic():
                patient, created = Patient.objects.get_or_create(
                    nom=nom,
                    prenom=prenom,
                    date_naissance=date_naissance,
                    defaults={
                        'sexe': sexe,
                        'telephone': telephone or '',
                        'email': email or '',
                        'adresse': adresse or '',
                    }
                )
                resultats['importes'] += 1
        except Exception as e:
            resultats['erreurs'].append({'ligne': row, 'erreur': str(e)})

    return resultats