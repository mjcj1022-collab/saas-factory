import uuid
from django.db import models


class Integration(models.Model):
    AUTH_TYPES = (
        ("oauth2", "OAuth2"),
        ("api_key", "API Key"),
        ("basic", "Basic Auth"),
        ("webhook", "Webhook"),
    )
    CATEGORIES = (
        ("accounting", "Accounting"),
        ("crm", "CRM"),
        ("gis", "GIS"),
        ("email", "Email"),
        ("sms", "SMS"),
        ("storage", "Storage"),
        ("scheduling", "Scheduling"),
        ("erp", "ERP"),
        ("iot", "IoT / Telematics"),
        ("payments", "Payments"),
        ("documents", "Documents"),
        ("project_mgmt", "Project Management"),
        ("lms", "LMS"),
    )

    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=100, choices=CATEGORIES)
    auth_type = models.CharField(max_length=50, choices=AUTH_TYPES)
    logo_url = models.URLField(blank=True)
    docs_url = models.URLField(blank=True)
    enabled = models.BooleanField(default=True)
    supported_verticals = models.JSONField(default=list)

    class Meta:
        db_table = "integrations"


class OrganizationIntegration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    credentials = models.JSONField(default=dict)
    config = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    connected_at = models.DateTimeField(auto_now_add=True)
    last_sync = models.DateTimeField(null=True)

    class Meta:
        db_table = "organization_integrations"
        unique_together = ("organization_id", "integration")


class WebhookEndpoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    url = models.URLField()
    secret = models.CharField(max_length=255)
    events = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "webhook_endpoints"
