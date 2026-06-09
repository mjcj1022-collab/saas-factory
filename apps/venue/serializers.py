from rest_framework import serializers
from .models import Venue, Room, VenueBooking, VendorAssignment, VenueInvoice

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'address', 'capacity', 'amenities']
        read_only_fields = ['id']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'venue', 'name', 'capacity', 'hourly_rate', 'features']
        read_only_fields = ['id']

class VenueBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueBooking
        fields = ['id', 'venue', 'room', 'event_name', 'client_name', 'client_email', 'event_date', 'start_time', 'end_time', 'guest_count', 'status', 'total_revenue', 'created_at']
        read_only_fields = ['id']

class VendorAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAssignment
        fields = ['id', 'booking', 'vendor_type', 'company_name', 'contact_email', 'load_in_time', 'confirmed']
        read_only_fields = ['id']

class VenueInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueInvoice
        fields = ['id', 'booking', 'subtotal', 'tax', 'total', 'status', 'sent_at', 'paid_at', 'created_at']
        read_only_fields = ['id']
