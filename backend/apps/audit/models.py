from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)  # CREATE, READ, UPDATE, DELETE, LOGIN, LOGOUT
    table_concernee = models.CharField(max_length=100)
    enregistrement_id = models.IntegerField()
    details = models.TextField(blank=True)
    ip_adresse = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur} - {self.action} - {self.table_concernee} #{self.enregistrement_id} - {self.timestamp}"