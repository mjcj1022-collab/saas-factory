import uuid
from django.db import models


class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    capacity = models.IntegerField()
    amenities = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "venue_venues"


class Room(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    features = models.JSONField(default=list)

    class Meta:
        db_table = "venue_rooms"


class VenueBooking(models.Model):
    STATUS = (
        ("inquiry", "Inquiry"),
        ("hold", "Hold"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    event_name = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    guest_count = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=STATUS, default="inquiry")
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "venue_bookings"


class VendorAssignment(models.Model):
    booking = models.ForeignKey(VenueBooking, on_delete=models.CASCADE, related_name="vendors")
    vendor_type = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True)
    load_in_time = models.TimeField(null=True)
    confirmed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "venue_vendor_assignments"


class VenueInvoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(VenueBooking, on_delete=models.CASCADE, related_name="invoices")
    line_items = models.JSONField(default=list)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="draft")
    sent_at = models.DateTimeField(null=True)
    paid_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "venue_invoices"
