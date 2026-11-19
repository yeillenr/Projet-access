from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class RendezVous(TimeStampedModel):
    STATUT_CHOICES = (
        ('PLANIFIE', 'Planifié'),
        ('CONFIRME', 'Confirmé'),
        ('EN_SALLE', 'En salle d\'attente'),
        ('EN_CONSULTATION', 'En consultation'),
        ('TERMINE', 'Terminé'),
        ('ANNULE', 'Annulé'),
        ('ABSENT', 'Absent'),
    )
    TYPE_CHOICES = (
        ('PREMIERE', 'Première visite'),
        ('SUIVI', 'Suivi'),
        ('URGENCE', 'Urgence'),
    )

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='rendezvous')
    praticien = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rendezvous_praticien', limit_choices_to={'role': 'MEDECIN'})
    date_heure = models.DateTimeField()
    duree = models.IntegerField(default=30, help_text="Durée en minutes")
    type_consultation = models.CharField(max_length=20, choices=TYPE_CHOICES, default='SUIVI')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='PLANIFIE')
    motif = models.TextField(blank=True)

    class Meta:
        ordering = ['date_heure']
        indexes = [models.Index(fields=['date_heure', 'praticien'])]

    def __str__(self):
        return f"RDV {self.patient} - {self.date_heure.strftime('%d/%m/%Y %H:%M')}"