from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class CompteRendu(TimeStampedModel):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='comptes_rendus')
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='compte_rendu', unique=True)
    date_redaction = models.DateTimeField(auto_now_add=True)
    contenu = models.TextField()
    modele_utilise = models.CharField(max_length=100, blank=True, help_text="Nom du modèle utilisé")

    def __str__(self):
        return f"CR {self.patient} - {self.date_redaction.strftime('%d/%m/%Y')}"