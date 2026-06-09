from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, TelemetryEventViewSet, WorkOrderViewSet, InventoryPartViewSet

router = DefaultRouter()
router.register("vehicles", VehicleViewSet, basename="vehicle")
router.register("telemetry", TelemetryEventViewSet, basename="telemetry")
router.register("work-orders", WorkOrderViewSet, basename="workorder")
router.register("inventory", InventoryPartViewSet, basename="inventory")

urlpatterns = [path("", include(router.urls))]
