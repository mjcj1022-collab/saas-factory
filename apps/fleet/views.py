from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Vehicle, TelemetryEvent, MaintenancePrediction, InventoryPart, WorkOrder
from .serializers import (
    VehicleSerializer, TelemetryEventSerializer,
    MaintenancePredictionSerializer, InventoryPartSerializer, WorkOrderSerializer,
)


class VehicleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VehicleSerializer

    def get_queryset(self):
        return Vehicle.objects.filter(organization_id=self.request.user.organization_id)

    @action(detail=True, methods=["post"])
    def analyze(self, request, pk=None):
        vehicle = self.get_object()
        from .services import PredictiveMaintenanceEngine, InventoryAutomation
        engine = PredictiveMaintenanceEngine()
        predictions = engine.save_predictions(str(vehicle.id))
        automation = InventoryAutomation()
        reorders = []
        for p in predictions:
            reorders.extend(automation.check_and_reorder(p))
        return Response({
            "predictions": MaintenancePredictionSerializer(predictions, many=True).data,
            "reorders_triggered": reorders,
        })

    @action(detail=False, methods=["get"])
    def fleet_health(self, request):
        vehicles = self.get_queryset()
        total = vehicles.count()
        critical = sum(1 for v in vehicles if v.predictions.filter(confidence__gte=0.8, acknowledged=False).exists())
        return Response({
            "total": total,
            "critical": critical,
            "healthy": total - critical,
        })


class TelemetryEventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TelemetryEventSerializer

    def get_queryset(self):
        return TelemetryEvent.objects.filter(
            vehicle__organization_id=self.request.user.organization_id
        ).order_by("-timestamp")[:500]


class WorkOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkOrderSerializer

    def get_queryset(self):
        return WorkOrder.objects.filter(
            vehicle__organization_id=self.request.user.organization_id
        ).select_related("vehicle").order_by("-created_at")

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        from django.utils import timezone
        wo = self.get_object()
        wo.status = "completed"
        wo.actual_cost = request.data.get("actual_cost", wo.estimated_cost)
        wo.labor_hours = request.data.get("labor_hours", wo.labor_hours)
        wo.completed_at = timezone.now()
        wo.save()
        return Response(WorkOrderSerializer(wo).data)


class InventoryPartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InventoryPartSerializer

    def get_queryset(self):
        return InventoryPart.objects.filter(organization_id=self.request.user.organization_id)

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        from django.db import models as dm
        parts = self.get_queryset().filter(quantity__lte=dm.F("reorder_point"))
        return Response(InventoryPartSerializer(parts, many=True).data)
