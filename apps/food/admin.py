from django.contrib import admin
from .models import Farm, HarvestLog, DeliveryRoute, Delivery

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(HarvestLog)
class HarvestLogAdmin(admin.ModelAdmin):
    list_display = ['farm', 'produce', 'quantity', 'harvest_date', 'quality_grade']
    list_filter = ['quality_grade']

@admin.register(DeliveryRoute)
class DeliveryRouteAdmin(admin.ModelAdmin):
    list_display = ['route_date', 'status', 'optimized']
    list_filter = ['status']

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['route', 'store', 'quantity_ordered', 'status']
    list_filter = ['status']
