import uuid
from django.db import models


class RentalProperty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    property_type = models.CharField(max_length=100, default="apartment")
    max_guests = models.IntegerField(default=2)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.FloatField(default=1)
    wifi_password = models.CharField(max_length=255, blank=True)
    door_code = models.CharField(max_length=100, blank=True)
    check_in_instructions = models.TextField(blank=True)
    house_rules = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "hospitality_properties"


class Reservation(models.Model):
    PLATFORMS = (
        ("airbnb", "Airbnb"),
        ("vrbo", "VRBO"),
        ("booking_com", "Booking.com"),
        ("direct", "Direct"),
    )
    STATUS = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("checked_in", "Checked In"),
        ("checked_out", "Checked Out"),
        ("canceled", "Canceled"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE, related_name="reservations")
    platform = models.CharField(max_length=50, choices=PLATFORMS)
    platform_reservation_id = models.CharField(max_length=255, blank=True)
    guest_name = models.CharField(max_length=255)
    guest_email = models.EmailField(blank=True)
    guest_count = models.IntegerField(default=1)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS, default="pending")
    nightly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "hospitality_reservations"


class GuestThread(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=50)  # "guest" | "host" | "ai"
    message = models.TextField()
    platform = models.CharField(max_length=50)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_automated = models.BooleanField(default=False)

    class Meta:
        db_table = "hospitality_guest_threads"


class SmartLockCode(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name="lock_code")
    code = models.CharField(max_length=20)
    lock_provider = models.CharField(max_length=50)
    external_id = models.CharField(max_length=255, blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    created = models.BooleanField(default=False)

    class Meta:
        db_table = "hospitality_lock_codes"


class CleaningJob(models.Model):
    STATUS = (
        ("scheduled", "Scheduled"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("skipped", "Skipped"),
    )

    property = models.ForeignKey(RentalProperty, on_delete=models.CASCADE, related_name="cleaning_jobs")
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, related_name="cleaning_jobs")
    scheduled_time = models.DateTimeField()
    cleaner_id = models.UUIDField(null=True)
    status = models.CharField(max_length=50, choices=STATUS, default="scheduled")
    checklist = models.JSONField(default=list)
    completed_at = models.DateTimeField(null=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "hospitality_cleaning_jobs"
