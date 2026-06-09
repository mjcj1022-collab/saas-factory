from django.contrib import admin
from .models import Property, Permit, Inspection

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['address', 'jurisdiction', 'utility_provider']
    search_fields = ['address', 'parcel_id']

@admin.register(Permit)
class PermitAdmin(admin.ModelAdmin):
    list_display = ['property', 'permit_type', 'status', 'permit_number']
    list_filter = ['status', 'permit_type']
    search_fields = ['permit_number']

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ['property', 'inspection_type', 'status', 'scheduled_date']
    list_filter = ['status']
