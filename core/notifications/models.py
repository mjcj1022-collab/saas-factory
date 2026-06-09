import uuid
from django.db import models


class NotificationTemplate(models.Model):
    CHANNELS = (
        ("email", "Email"),
        ("sms", "SMS"),
        ("slack", "Slack"),
        ("push", "Push"),
        ("teams", "MS Teams"),
    )

    name = models.CharField(max_length=255, unique=True)
    channel = models.CharField(max_length=50, choices=CHANNELS)
    subject_template = models.CharField(max_length=500, blank=True)
    body_template = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "notification_templates"


class Notification(models.Model):
    CHANNELS = (
        ("email", "Email"),
        ("sms", "SMS"),
        ("slack", "Slack"),
        ("push", "Push"),
        ("teams", "MS Teams"),
    )
    STATUS = (
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    channel = models.CharField(max_length=50, choices=CHANNELS)
    recipient = models.CharField(max_length=255)
    subject = models.CharField(max_length=500, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS, default="pending")
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True)
    error = models.TextField(blank=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]


class NotificationPreference(models.Model):
    user_id = models.UUIDField(db_index=True)
    organization_id = models.UUIDField()
    event_type = models.CharField(max_length=200)
    channels = models.JSONField(default=list)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = "notification_preferences"
        unique_together = ("user_id", "event_type")
