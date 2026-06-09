import uuid
from django.db import models


class FranchiseBrand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    logo_url = models.URLField(blank=True)
    royalty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "franchise_brands"


class Franchisee(models.Model):
    STATUS = (
        ("applicant", "Applicant"),
        ("screening", "Screening"),
        ("approved", "Approved"),
        ("active", "Active"),
        ("terminated", "Terminated"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey(FranchiseBrand, on_delete=models.CASCADE, related_name="franchisees")
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default="applicant")
    net_worth = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    liquid_capital = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "franchise_franchisees"


class FranchiseLocation(models.Model):
    LAUNCH_STATUS = (
        ("pipeline", "Pipeline"),
        ("site_selection", "Site Selection"),
        ("lease_negotiation", "Lease Negotiation"),
        ("construction", "Construction"),
        ("training", "Training"),
        ("pre_open", "Pre-Open"),
        ("open", "Open"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    franchisee = models.ForeignKey(Franchisee, on_delete=models.CASCADE, related_name="locations")
    address = models.TextField()
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    opening_date = models.DateField(null=True)
    launch_status = models.CharField(max_length=50, choices=LAUNCH_STATUS, default="pipeline")
    target_open_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "franchise_locations"


class Milestone(models.Model):
    location = models.ForeignKey(FranchiseLocation, on_delete=models.CASCADE, related_name="milestones")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True)
    sequence = models.IntegerField(default=0)

    class Meta:
        db_table = "franchise_milestones"
        ordering = ["sequence"]


class ComplianceScore(models.Model):
    RISK_LEVELS = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    )

    location = models.OneToOneField(FranchiseLocation, on_delete=models.CASCADE, related_name="compliance_score")
    score = models.FloatField(default=100.0)
    risk_level = models.CharField(max_length=50, choices=RISK_LEVELS, default="low")
    findings = models.JSONField(default=list)
    last_assessed = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "franchise_compliance_scores"


class TrainingModule(models.Model):
    brand = models.ForeignKey(FranchiseBrand, on_delete=models.CASCADE, related_name="training_modules")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content_type = models.CharField(max_length=50, default="video")
    content_url = models.URLField(blank=True)
    duration_minutes = models.IntegerField(default=0)
    is_required = models.BooleanField(default=True)
    sequence = models.IntegerField(default=0)

    class Meta:
        db_table = "franchise_training_modules"


class TrainingCompletion(models.Model):
    employee_id = models.UUIDField()
    location = models.ForeignKey(FranchiseLocation, on_delete=models.CASCADE)
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True)

    class Meta:
        db_table = "franchise_training_completions"
        unique_together = ("employee_id", "module")


class ConstructionPhase(models.Model):
    location = models.ForeignKey(FranchiseLocation, on_delete=models.CASCADE, related_name="construction_phases")
    phase_name = models.CharField(max_length=255)
    percent_complete = models.IntegerField(default=0)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "franchise_construction_phases"
