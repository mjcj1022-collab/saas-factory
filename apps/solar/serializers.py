from rest_framework import serializers
from .models import Property, RoofPlane, SolarArray, Permit, SetbackValidation, Inspection

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'address', 'latitude', 'longitude', 'parcel_id', 'jurisdiction', 'utility_provider']
        read_only_fields = ['id']

class RoofPlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoofPlane
        fields = ['id', 'property', 'area_sqft', 'azimuth', 'pitch', 'usable_area_sqft']
        read_only_fields = ['id']

class SolarArraySerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarArray
        fields = ['id', 'roof', 'panel_count', 'system_kw', 'estimated_annual_kwh']
        read_only_fields = ['id']

class PermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permit
        fields = ['id', 'property', 'permit_type', 'jurisdiction', 'status', 'permit_number', 'submitted_at', 'approved_at']
        read_only_fields = ['id']

class SetbackValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetbackValidation
        fields = ['id', 'property', 'rule_type', 'required_ft', 'actual_ft', 'passed']
        read_only_fields = ['id']

class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspection
        fields = ['id', 'property', 'inspection_type', 'scheduled_date', 'status', 'inspector_name']
        read_only_fields = ['id']
