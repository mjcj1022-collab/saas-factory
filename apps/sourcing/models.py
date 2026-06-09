import uuid
from django.db import models


class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    company_name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    platform = models.CharField(max_length=100, default="direct")
    rating = models.FloatField(default=0)
    verified = models.BooleanField(default=False)
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sourcing_suppliers"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    unit_of_measure = models.CharField(max_length=50, default="unit")
    preferred_supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    target_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sourcing_products"


class SupplierQuote(models.Model):
    STATUS = (
        ("requested", "Requested"),
        ("received", "Received"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="quotes")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="quotes")
    status = models.CharField(max_length=50, choices=STATUS, default="requested")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    moq = models.IntegerField(null=True)
    lead_time_days = models.IntegerField(null=True)
    notes = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "sourcing_quotes"


class ProductionRun(models.Model):
    STATUS = (
        ("planned", "Planned"),
        ("in_production", "In Production"),
        ("quality_check", "Quality Check"),
        ("shipped", "Shipped"),
        ("received", "Received"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="production_runs")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS, default="planned")
    start_date = models.DateField(null=True)
    expected_ship_date = models.DateField(null=True)
    actual_ship_date = models.DateField(null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_cost = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sourcing_production_runs"


class Shipment(models.Model):
    production_run = models.ForeignKey(ProductionRun, on_delete=models.CASCADE, related_name="shipments")
    tracking_number = models.CharField(max_length=255, blank=True)
    carrier = models.CharField(max_length=100, blank=True)
    shipped_at = models.DateTimeField(null=True)
    estimated_arrival = models.DateField(null=True)
    arrived_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=50, default="in_transit")

    class Meta:
        db_table = "sourcing_shipments"
