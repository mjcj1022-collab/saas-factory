import uuid
from django.db import models


class Farm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact_name = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    certifications = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "food_farms"


class Produce(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, default="lb")
    avg_shelf_life_days = models.IntegerField(default=7)

    class Meta:
        db_table = "food_produce"


class HarvestLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="harvests")
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.FloatField()
    harvest_date = models.DateField()
    quality_grade = models.CharField(max_length=10, default="A")
    available_quantity = models.FloatField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "food_harvest_logs"


class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "food_stores"


class DeliveryRoute(models.Model):
    STATUS = (
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    route_date = models.DateField()
    driver_id = models.UUIDField(null=True)
    vehicle_id = models.UUIDField(null=True)
    stops = models.JSONField(default=list)
    total_distance_miles = models.FloatField(default=0)
    status = models.CharField(max_length=50, choices=STATUS, default="planned")
    optimized = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "food_delivery_routes"


class Delivery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey(DeliveryRoute, on_delete=models.CASCADE, related_name="deliveries")
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    harvest = models.ForeignKey(HarvestLog, on_delete=models.CASCADE)
    quantity_ordered = models.FloatField()
    quantity_delivered = models.FloatField(default=0)
    status = models.CharField(max_length=50, default="pending")
    delivered_at = models.DateTimeField(null=True)
    signature_url = models.URLField(blank=True)

    class Meta:
        db_table = "food_deliveries"
