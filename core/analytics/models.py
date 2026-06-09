import uuid
from django.db import models


class AnalyticsEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    user_id = models.UUIDField(null=True)
    event_name = models.CharField(max_length=255, db_index=True)
    properties = models.JSONField(default=dict)
    session_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "analytics_events"
        ordering = ["-created_at"]


class KPISnapshot(models.Model):
    organization_id = models.UUIDField(db_index=True)
    vertical = models.CharField(max_length=100)
    metric_name = models.CharField(max_length=255)
    metric_value = models.FloatField()
    period = models.DateField(db_index=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "kpi_snapshots"


class Dashboard(models.Model):
    organization_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=255)
    vertical = models.CharField(max_length=100)
    config = models.JSONField(default=dict)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "dashboards"
