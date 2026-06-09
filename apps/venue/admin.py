from django.contrib import admin
from .models import Venue, VenueBooking, VenueInvoice

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'capacity']
    search_fields = ['name']

@admin.register(VenueBooking)
class VenueBookingAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'client_name', 'event_date', 'status']
    list_filter = ['status']
    search_fields = ['event_name', 'client_name']

@admin.register(VenueInvoice)
class VenueInvoiceAdmin(admin.ModelAdmin):
    list_display = ['booking', 'total', 'status']
    list_filter = ['status']
