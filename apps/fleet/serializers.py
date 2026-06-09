from rest_framework import serializers
from .models import Vehicle, TelemetryEvent, MaintenancePrediction, InventoryPart, WorkOrder


class VehicleSerializer(serializers.ModelSerializer):
    health_score = serializers.SerializerMethodField()
    open_work_orders = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = [
            "id", "vin", "make", "model", "year", "vehicle_type",
            "odometer", "engine_hours", "license_plate", "is_active",
            "last_seen_at", "health_score", "open_work_orders",
        ]
        read_only_fields = ["id"]

    def get_health_score(self, obj):
        critical = obj.predictions.filter(confidence__gte=0.8, acknowledged=False).count()
        if critical >= 3:
            return "critical"
        elif critical >= 1:
            return "warning"
        return "good"

    def get_open_work_orders(self, obj):
        return obj.work_orders.filter(status__in=["open", "in_progress", "waiting_parts"]).count()

    def create(self, validated_data):
        validated_data["organization_id"] = self.context["request"].user.organization_id
        return super().create(validated_data)


class TelemetryEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemetryEvent
        fields = ["id", "vehicle", "code", "description", "severity", "payload", "latitude", "longitude", "timestamp"]
        read_only_fields = ["id"]


class MaintenancePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenancePrediction
        fields = ["id", "predicted_failure", "component", "confidence", "predicted_days", "predicted_at", "acknowledged"]
        read_only_fields = ["id", "predicted_at"]


class InventoryPartSerializer(serializers.ModelSerializer):
    needs_reorder = serializers.SerializerMethodField()

    class Meta:
        model = InventoryPart
        fields = ["id", "sku", "name", "quantity", "reorder_point", "unit_cost", "supplier", "location", "needs_reorder"]
        read_only_fields = ["id"]

    def get_needs_reorder(self, obj):
        return obj.quantity <= obj.reorder_point

    def create(self, validated_data):
        validated_data["organization_id"] = self.context["request"].user.organization_id
        return super().create(validated_data)


class WorkOrderSerializer(serializers.ModelSerializer):
    vehicle_info = serializers.SerializerMethodField()

    class Meta:
        model = WorkOrder
        fields = [
            "id", "vehicle", "vehicle_info", "status", "description",
            "assigned_mechanic_id", "parts_used", "labor_hours",
            "estimated_cost", "actual_cost", "scheduled_date", "completed_at", "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_vehicle_info(self, obj):
        v = obj.vehicle
        return f"{v.year} {v.make} {v.model} ({v.vin[-6:]})"
