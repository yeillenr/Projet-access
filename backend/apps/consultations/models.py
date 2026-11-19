from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class Consultation(TimeStampedModel):
    STATUT_PAIEMENT_CHOICES = (
        ('IMPAYE', 'Impayé'),
        ('PARTIEL', 'Partiellement payé'),
        ('PAYE', 'Payé'),
    )

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='consultations')
    praticien = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consultations', limit_choices_to={'role': 'MEDECIN'})
    date_consultation = models.DateTimeField(auto_now_add=True)
    motif = models.TextField()
    duree_effective = models.IntegerField(blank=True, null=True, help_text="Durée réelle en minutes")
    statut_paiement = models.CharField(max_length=10, choices=STATUT_PAIEMENT_CHOICES, default='IMPAYE')

    class Meta:
        ordering = ['-date_consultation']

    def __str__(self):
        return f"Consultation {self.patient} - {self.date_consultation.strftime('%d/%m/%Y')}"

    @property
    def montant_total(self):
        total = self.actes_factures.aggregate(
            total=models.Sum(models.F('tarif_applique') * models.F('quantite'))
        )['total']
        return total or 0

class ParametresVitaux(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='parametres')
    date_mesure = models.DateTimeField(auto_now_add=True)
    tension_sys = models.IntegerField(blank=True, null=True)
    tension_dia = models.IntegerField(blank=True, null=True)
    frequence_cardiaque = models.IntegerField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    poids = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    taille = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Taille en cm")
    # IMC calculé automatiquement
    perimetre_cervical = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    perimetre_abdominal = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    saturation_oxygene = models.IntegerField(blank=True, null=True)
    autres = models.TextField(blank=True)

    @property
    def imc(self):
        if self.poids and self.taille and self.taille > 0:
            return round(self.poids / ((self.taille/100) ** 2), 2)
        return None

class Pathologie(models.Model):
    code_cim10 = models.CharField(max_length=10, unique=True)
    libelle = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code_cim10} - {self.libelle}"

class ConsultationPathologie(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='diagnostics')
    pathologie = models.ForeignKey(Pathologie, on_delete=models.CASCADE)
    est_principal = models.BooleanField(default=False)
    statut = models.CharField(max_length=20, choices=(('EN_COURS', 'En cours'), ('GUERIE', 'Guérie'), ('CHRONIQUE', 'Chronique')), default='EN_COURS')

    class Meta:
        unique_together = ('consultation', 'pathologie')