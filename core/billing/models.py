import uuid
from django.db import models


class Subscription(models.Model):
    PLANS = (
        ("starter", "Starter"),
        ("growth", "Growth"),
        ("enterprise", "Enterprise"),
    )
    STATUS = (
        ("active", "Active"),
        ("canceled", "Canceled"),
        ("past_due", "Past Due"),
        ("trialing", "Trialing"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True)
    plan = models.CharField(max_length=50, choices=PLANS, default="starter")
    status = models.CharField(max_length=50, choices=STATUS, default="trialing")
    current_period_start = models.DateTimeField(null=True)
    current_period_end = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subscriptions"


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    stripe_invoice_id = models.CharField(max_length=255, blank=True)
    amount_cents = models.IntegerField()
    currency = models.CharField(max_length=3, default="usd")
    status = models.CharField(max_length=50, default="draft")
    paid_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "invoices"


class UsageRecord(models.Model):
    organization_id = models.UUIDField(db_index=True)
    feature = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "usage_records"
