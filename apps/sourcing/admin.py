from django.contrib import admin
from .models import Supplier, Product, ProductionRun, Shipment

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'country', 'verified', 'rating']
    list_filter = ['verified', 'country']
    search_fields = ['company_name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category']
    list_filter = ['category']
    search_fields = ['sku', 'name']

@admin.register(ProductionRun)
class ProductionRunAdmin(admin.ModelAdmin):
    list_display = ['product', 'supplier', 'quantity', 'status']
    list_filter = ['status']

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['production_run', 'carrier', 'status', 'shipped_at']
    list_filter = ['status']
