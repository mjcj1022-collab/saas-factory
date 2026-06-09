import uuid
from django.db import models


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    company_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    billing_email = models.EmailField(blank=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    monthly_retainer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "agency_clients"


class AgencyProject(models.Model):
    STATUS = (
        ("active", "Active"),
        ("on_hold", "On Hold"),
        ("completed", "Completed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default="active")
    start_date = models.DateField(null=True)
    deadline = models.DateField(null=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "agency_projects"


class Asset(models.Model):
    TYPES = (
        ("design", "Design"),
        ("copy", "Copy"),
        ("video", "Video"),
        ("code", "Code"),
        ("document", "Document"),
        ("image", "Image"),
    )
    STATUS = (
        ("in_progress", "In Progress"),
        ("review", "In Review"),
        ("revision_requested", "Revision Requested"),
        ("approved", "Approved"),
        ("locked", "Locked"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(AgencyProject, on_delete=models.CASCADE, related_name="assets")
    name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=50, choices=TYPES)
    status = models.CharField(max_length=50, choices=STATUS, default="in_progress")
    file_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "agency_assets"


class AssetVersion(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="versions")
    version_number = models.IntegerField(default=1)
    file_url = models.URLField()
    notes = models.TextField(blank=True)
    created_by_id = models.UUIDField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "agency_asset_versions"
        ordering = ["-version_number"]


class ApprovalRequest(models.Model):
    STATUS = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("revision_requested", "Revision Requested"),
    )

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="approvals")
    version = models.ForeignKey(AssetVersion, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS, default="pending")
    client_notes = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "agency_approvals"


class AgencyInvoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="invoices")
    project = models.ForeignKey(AgencyProject, on_delete=models.SET_NULL, null=True)
    line_items = models.JSONField(default=list)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, default="draft")
    due_date = models.DateField(null=True)
    paid_at = models.DateTimeField(null=True)
    stripe_invoice_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "agency_invoices"
