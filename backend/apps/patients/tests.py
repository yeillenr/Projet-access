import os
import tempfile
from django.test import TestCase
from openpyxl import Workbook

from apps.patients.import_excel import importer_patients_excel
from apps.patients.models import Patient


class PatientImportTests(TestCase):
    def test_importer_detects_duplicates_and_reports(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(['nom', 'prenom', 'date_naissance', 'sexe', 'telephone', 'email', 'adresse'])
        sheet.append(['Dupont', 'Jean', '1980-01-01', 'M', '0600000000', 'jean@example.com', 'Paris'])
        sheet.append(['Dupont', 'Jean', '1980-01-01', 'M', '0600000000', 'jean@example.com', 'Paris'])

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as handle:
            workbook.save(handle.name)
            temp_path = handle.name

        try:
            result = importer_patients_excel(temp_path, None)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        self.assertEqual(result['importes'], 1)
        self.assertEqual(result['doublons'], 1)
        self.assertEqual(Patient.objects.count(), 1)
