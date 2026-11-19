from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrateur'),
        ('MEDECIN', 'Médecin'),
        ('SECRETAIRE', 'Secrétaire'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEDECIN')
    telephone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def nom_complet(self):
        return f"{self.last_name} {self.first_name}"