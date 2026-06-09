from django.contrib import admin
from .models import Vehicle, WorkOrder, InventoryPart, TelemetryEvent, MaintenancePrediction

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vin', 'make', 'model', 'year', 'is_active']
    list_filter = ['make', 'vehicle_type']
    search_fields = ['vin', 'make', 'model']

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'status', 'estimated_cost', 'created_at']
    list_filter = ['status']

@admin.register(InventoryPart)
class InventoryPartAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'quantity', 'reorder_point']
    search_fields = ['sku', 'name']

@admin.register(TelemetryEvent)
class TelemetryEventAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'code', 'severity', 'timestamp']
    list_filter = ['severity']
    search_fields = ['code']

@admin.register(MaintenancePrediction)
class MaintenancePredictionAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'predicted_failure', 'confidence', 'predicted_days', 'acknowledged']
    list_filter = ['acknowledged']
