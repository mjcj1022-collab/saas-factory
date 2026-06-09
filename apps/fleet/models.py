import uuid
from django.db import models


class Vehicle(models.Model):
    TYPES = (
        ("truck", "Truck"),
        ("van", "Van"),
        ("car", "Car"),
        ("trailer", "Trailer"),
        ("heavy_equipment", "Heavy Equipment"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    vin = models.CharField(max_length=17, unique=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vehicle_type = models.CharField(max_length=50, choices=TYPES)
    odometer = models.IntegerField(default=0)
    engine_hours = models.FloatField(default=0)
    license_plate = models.CharField(max_length=50, blank=True)
    assigned_driver_id = models.UUIDField(null=True)
    is_active = models.BooleanField(default=True)
    last_seen_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "fleet_vehicles"


class TelemetryEvent(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="telemetry")
    code = models.CharField(max_length=50, db_index=True)
    description = models.CharField(max_length=255, blank=True)
    payload = models.JSONField(default=dict)
    severity = models.CharField(max_length=50, default="info")
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    timestamp = models.DateTimeField(db_index=True)

    class Meta:
        db_table = "fleet_telemetry_events"
        ordering = ["-timestamp"]


class MaintenancePrediction(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="predictions")
    predicted_failure = models.CharField(max_length=255)
    component = models.CharField(max_length=255, blank=True)
    confidence = models.FloatField()
    predicted_days = models.IntegerField()
    predicted_at = models.DateTimeField(auto_now_add=True)
    acknowledged = models.BooleanField(default=False)

    class Meta:
        db_table = "fleet_maintenance_predictions"


class InventoryPart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    reorder_point = models.IntegerField(default=5)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    supplier = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "fleet_inventory_parts"
        unique_together = ("organization_id", "sku")


class WorkOrder(models.Model):
    STATUS = (
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("waiting_parts", "Waiting Parts"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="work_orders")
    status = models.CharField(max_length=50, choices=STATUS, default="open")
    description = models.TextField()
    assigned_mechanic_id = models.UUIDField(null=True)
    parts_used = models.JSONField(default=list)
    labor_hours = models.FloatField(default=0)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    scheduled_date = models.DateField(null=True)
    completed_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "fleet_work_orders"
