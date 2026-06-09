import uuid
from django.db import models


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    parcel_id = models.CharField(max_length=100, blank=True)
    jurisdiction = models.CharField(max_length=255, blank=True)
    utility_provider = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "solar_properties"


class RoofPlane(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="roof_planes")
    geometry = models.JSONField(default=dict)
    area_sqft = models.FloatField(default=0)
    azimuth = models.FloatField()
    pitch = models.FloatField()
    usable_area_sqft = models.FloatField(default=0)

    class Meta:
        db_table = "solar_roof_planes"


class SolarArray(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roof = models.ForeignKey(RoofPlane, on_delete=models.CASCADE, related_name="arrays")
    panel_model = models.CharField(max_length=255, blank=True)
    panel_count = models.IntegerField()
    system_kw = models.FloatField()
    estimated_annual_kwh = models.FloatField(default=0)
    tilt = models.FloatField(default=0)
    azimuth = models.FloatField(default=180)

    class Meta:
        db_table = "solar_arrays"


class Permit(models.Model):
    STATUS = (
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("expired", "Expired"),
    )
    TYPES = (
        ("building", "Building Permit"),
        ("electrical", "Electrical Permit"),
        ("interconnection", "Utility Interconnection"),
        ("net_metering", "Net Metering Application"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="permits")
    permit_type = models.CharField(max_length=50, choices=TYPES)
    jurisdiction = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS, default="draft")
    permit_number = models.CharField(max_length=100, blank=True)
    submitted_at = models.DateTimeField(null=True)
    approved_at = models.DateTimeField(null=True)
    expires_at = models.DateTimeField(null=True)
    documents = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "solar_permits"


class SetbackValidation(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="setback_validations")
    rule_type = models.CharField(max_length=100)
    required_ft = models.FloatField()
    actual_ft = models.FloatField()
    passed = models.BooleanField()
    notes = models.TextField(blank=True)
    validated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "solar_setback_validations"


class Inspection(models.Model):
    STATUS = (
        ("scheduled", "Scheduled"),
        ("passed", "Passed"),
        ("failed", "Failed"),
        ("reinspection", "Re-inspection Required"),
    )

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="inspections")
    inspection_type = models.CharField(max_length=100)
    scheduled_date = models.DateField(null=True)
    status = models.CharField(max_length=50, choices=STATUS, default="scheduled")
    inspector_name = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "solar_inspections"
