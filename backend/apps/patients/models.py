from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, SoftDeleteModel

class Patient(TimeStampedModel, SoftDeleteModel):
    SEXE_CHOICES = (('M', 'Masculin'), ('F', 'Féminin'))
    STATUT_CHOICES = (('ACTIF', 'Actif'), ('INACTIF', 'Inactif'), ('DECEDE', 'Décédé'))

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)
    groupe_sanguin = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    antecedents = models.TextField(blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='ACTIF')
    corporate = models.BooleanField(default=False)
    vivant = models.BooleanField(default=True)
    annee_creation = models.DateField(auto_now_add=True)
    medecin_traitant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients_traites',
        limit_choices_to={'role': 'MEDECIN'}
    )

    class Meta:
        indexes = [
            models.Index(fields=['nom', 'prenom']),
            models.Index(fields=['telephone']),
            models.Index(fields=['date_naissance']),
        ]
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    @property
    def nom_complet(self):
        return f"{self.nom} {self.prenom}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_naissance.year - ((today.month, today.day) < (self.date_naissance.month, self.date_naissance.day))