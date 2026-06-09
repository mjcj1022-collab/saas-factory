from rest_framework import serializers
from .models import RentalProperty, Reservation, GuestThread, CleaningJob

class RentalPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalProperty
        fields = ['id', 'name', 'address', 'property_type', 'max_guests', 'bedrooms', 'bathrooms', 'is_active']
        read_only_fields = ['id']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'property', 'guest_name', 'guest_email', 'check_in', 'check_out', 'status', 'platform', 'total_revenue', 'created_at']
        read_only_fields = ['id']

class GuestThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestThread
        fields = ['id', 'reservation', 'sender', 'message', 'platform', 'sent_at', 'is_automated']
        read_only_fields = ['id']

class CleaningJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningJob
        fields = ['id', 'property', 'reservation', 'scheduled_time', 'status', 'completed_at']
        read_only_fields = ['id']
