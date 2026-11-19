from .models import AuditLog


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def log_action(request, action, table, record_id, details='', actor=None):
    if actor is None:
        actor = getattr(request, 'user', None)
        if not getattr(actor, 'is_authenticated', False):
            actor = None
    user = actor
    AuditLog.objects.create(
        utilisateur=user,
        action=action,
        table_concernee=table,
        enregistrement_id=record_id or 0,
        details=details,
        ip_adresse=get_client_ip(request),
    )


class AuditLogMixin:
    """Journalise automatiquement les créations, modifications et suppressions d'un ViewSet.

    Ne couvre pas les ViewSets qui redéfinissent create()/perform_destroy() sans
    appeler super() : dans ce cas, appeler log_action() directement.
    """
    audit_table_name = None

    def _audit_table(self):
        return self.audit_table_name or self.get_queryset().model._meta.db_table

    def perform_create(self, serializer):
        super().perform_create(serializer)
        log_action(self.request, 'CREATE', self._audit_table(), serializer.instance.pk)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        log_action(self.request, 'UPDATE', self._audit_table(), serializer.instance.pk)

    def perform_destroy(self, instance):
        record_id = instance.pk
        super().perform_destroy(instance)
        log_action(self.request, 'DELETE', self._audit_table(), record_id)
