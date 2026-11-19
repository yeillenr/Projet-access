from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class Ordonnance(TimeStampedModel):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='ordonnances')
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='ordonnance', unique=True)
    date_ordonnance = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ordonnance {self.id} - {self.patient} - {self.date_ordonnance.strftime('%d/%m/%Y')}"

class LigneOrdonnance(models.Model):
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE, related_name='lignes')
    medicament = models.CharField(max_length=255)
    posologie = models.CharField(max_length=255)
    duree = models.CharField(max_length=100, blank=True)
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicament} - {self.posologie}"