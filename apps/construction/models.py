import uuid
from django.db import models


class Project(models.Model):
    STATUS = (
        ("planning", "Planning"),
        ("active", "Active"),
        ("on_hold", "On Hold"),
        ("completed", "Completed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    project_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default="planning")
    start_date = models.DateField(null=True)
    completion_date = models.DateField(null=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "construction_projects"


class Drawing(models.Model):
    DISCIPLINES = (
        ("architectural", "Architectural"),
        ("structural", "Structural"),
        ("mep", "MEP"),
        ("civil", "Civil"),
        ("electrical", "Electrical"),
        ("plumbing", "Plumbing"),
        ("hvac", "HVAC"),
        ("fire_protection", "Fire Protection"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="drawings")
    drawing_number = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    discipline = models.CharField(max_length=100, choices=DISCIPLINES)
    file = models.FileField(upload_to="drawings/")
    revision = models.CharField(max_length=50)
    revision_date = models.DateField(null=True)
    uploaded_by_id = models.UUIDField(null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "construction_drawings"
        ordering = ["-uploaded_at"]


class RevisionAnalysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    old_drawing = models.ForeignKey(Drawing, related_name="previous_analyses", on_delete=models.CASCADE)
    new_drawing = models.ForeignKey(Drawing, related_name="current_analyses", on_delete=models.CASCADE)
    differences = models.JSONField(default=dict)
    ai_summary = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "construction_revision_analyses"


class TradePackage(models.Model):
    TRADES = (
        ("electrical", "Electrical"),
        ("hvac", "HVAC"),
        ("plumbing", "Plumbing"),
        ("concrete", "Concrete"),
        ("framing", "Framing"),
        ("drywall", "Drywall"),
        ("roofing", "Roofing"),
        ("structural", "Structural"),
        ("fire_protection", "Fire Protection"),
        ("millwork", "Millwork"),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="trade_packages")
    trade_type = models.CharField(max_length=100, choices=TRADES)
    company_name = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = "construction_trade_packages"


class MaterialImpact(models.Model):
    revision = models.ForeignKey(RevisionAnalysis, on_delete=models.CASCADE, related_name="material_impacts")
    trade = models.ForeignKey(TradePackage, on_delete=models.CASCADE)
    material_name = models.CharField(max_length=255)
    quantity_delta = models.FloatField()
    unit = models.CharField(max_length=50, blank=True)
    estimated_cost_delta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "construction_material_impacts"


class DailyReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="daily_reports")
    report_date = models.DateField()
    weather = models.CharField(max_length=100, blank=True)
    crew_count = models.IntegerField(default=0)
    progress_notes = models.TextField(blank=True)
    issues = models.JSONField(default=list)
    photos = models.JSONField(default=list)
    submitted_by_id = models.UUIDField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "construction_daily_reports"


class PunchItem(models.Model):
    STATUS = (
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="punch_items")
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS, default="open")
    assigned_trade = models.ForeignKey(TradePackage, on_delete=models.SET_NULL, null=True)
    due_date = models.DateField(null=True)
    photos = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "construction_punch_items"
