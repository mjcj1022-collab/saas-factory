from rest_framework import serializers
from .models import Supplier, Product, SupplierQuote, ProductionRun, Shipment

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'company_name', 'country', 'contact_name', 'contact_email', 'rating', 'verified', 'tags']
        read_only_fields = ['id']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'category', 'unit_of_measure', 'target_cost']
        read_only_fields = ['id']

class SupplierQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierQuote
        fields = ['id', 'supplier', 'product', 'status', 'unit_price', 'moq', 'lead_time_days', 'requested_at']
        read_only_fields = ['id']

class ProductionRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionRun
        fields = ['id', 'product', 'supplier', 'quantity', 'status', 'start_date', 'expected_ship_date', 'total_cost']
        read_only_fields = ['id']

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['id', 'production_run', 'tracking_number', 'carrier', 'status', 'shipped_at', 'estimated_arrival']
        read_only_fields = ['id']
