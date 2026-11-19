from django.db import models
from django.db.models import Q
from apps.core.models import TimeStampedModel

class ActeMedical(TimeStampedModel):
    code = models.CharField(max_length=20, unique=True)
    libelle = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.libelle}"

class Tarification(models.Model):
    acte = models.ForeignKey(ActeMedical, on_delete=models.CASCADE, related_name='tarifs')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_effet = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_effet']

    def __str__(self):
        return f"{self.acte.libelle} - {self.montant} FCFA (à partir du {self.date_effet})"

    @classmethod
    def tarif_en_vigueur(cls, acte, a_la_date):
        """Retourne la tarification applicable à un acte pour une date donnée."""
        return cls.objects.filter(
            acte=acte, date_effet__lte=a_la_date
        ).filter(
            Q(date_fin__isnull=True) | Q(date_fin__gte=a_la_date)
        ).order_by('-date_effet').first()


class ConsultationActe(models.Model):
    """Association d'un acte médical à une consultation, avec le tarif figé à la date d'application."""
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.CASCADE, related_name='actes_factures')
    acte = models.ForeignKey(ActeMedical, on_delete=models.PROTECT, related_name='consultations_liees')
    tarif_applique = models.DecimalField(max_digits=10, decimal_places=2, help_text="Montant figé au moment de la facturation")
    quantite = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.acte.libelle} x{self.quantite} - Consultation #{self.consultation_id}"