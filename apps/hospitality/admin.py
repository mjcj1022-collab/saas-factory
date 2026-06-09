from django.contrib import admin
from .models import RentalProperty, Reservation, CleaningJob

@admin.register(RentalProperty)
class RentalPropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'property_type', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'address']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['property', 'guest_name', 'platform', 'status', 'check_in', 'check_out']
    list_filter = ['status', 'platform']
    search_fields = ['guest_name']

@admin.register(CleaningJob)
class CleaningJobAdmin(admin.ModelAdmin):
    list_display = ['property', 'scheduled_time', 'status']
    list_filter = ['status']
