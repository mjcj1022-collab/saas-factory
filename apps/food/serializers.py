from rest_framework import serializers
from .models import Farm, Produce, HarvestLog, Store, DeliveryRoute, Delivery

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'contact_name', 'is_active']
        read_only_fields = ['id']

class ProduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = ['id', 'name', 'category', 'unit', 'avg_shelf_life_days']
        read_only_fields = ['id']

class HarvestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarvestLog
        fields = ['id', 'farm', 'produce', 'quantity', 'harvest_date', 'quality_grade', 'available_quantity']
        read_only_fields = ['id']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'is_active']
        read_only_fields = ['id']

class DeliveryRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryRoute
        fields = ['id', 'route_date', 'status', 'total_distance_miles', 'optimized', 'created_at']
        read_only_fields = ['id']

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'route', 'store', 'harvest', 'quantity_ordered', 'quantity_delivered', 'status', 'delivered_at']
        read_only_fields = ['id']
