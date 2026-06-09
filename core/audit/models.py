import uuid
from django.db import models


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    actor_id = models.UUIDField(null=True)
    actor_email = models.CharField(max_length=255, blank=True)
    action = models.CharField(max_length=255, db_index=True)
    object_type = models.CharField(max_length=100, db_index=True)
    object_id = models.CharField(max_length=100)
    before_state = models.JSONField(null=True)
    after_state = models.JSONField(null=True)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "audit_logs"
        ordering = ["-timestamp"]

    @classmethod
    def log(cls, organization_id, actor_id, action, object_type, object_id,
            before_state=None, after_state=None, ip_address=None, actor_email=""):
        return cls.objects.create(
            organization_id=organization_id,
            actor_id=actor_id,
            actor_email=actor_email,
            action=action,
            object_type=object_type,
            object_id=str(object_id),
            before_state=before_state,
            after_state=after_state,
            ip_address=ip_address,
        )
