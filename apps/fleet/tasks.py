from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def run_predictive_analysis_task(self, vehicle_id: str):
    """Run predictive maintenance analysis for a vehicle."""
    try:
        from apps.fleet.services import PredictiveMaintenanceEngine, InventoryAutomation
        from core.notifications.models import Notification
        from apps.fleet.models import Vehicle

        vehicle = Vehicle.objects.get(id=vehicle_id)
        engine = PredictiveMaintenanceEngine()
        predictions = engine.save_predictions(vehicle_id)

        automation = InventoryAutomation()
        all_reorders = []
        for pred in predictions:
            reorders = automation.check_and_reorder(pred)
            all_reorders.extend(reorders)

        if predictions:
            critical = [p for p in predictions if p.confidence >= 0.8]
            if critical:
                Notification.objects.create(
                    organization_id=vehicle.organization_id,
                    channel="email",
                    recipient="fleet_manager",
                    subject=f"Critical maintenance alert: {vehicle.year} {vehicle.make} {vehicle.model}",
                    message="\n".join([
                        f"• {p.predicted_failure} — {int(p.confidence * 100)}% confidence, {p.predicted_days} days"
                        for p in critical
                    ]),
                )

        logger.info("Fleet analysis complete for %s: %d predictions, %d reorders",
                    vehicle_id, len(predictions), len(all_reorders))
        return {"predictions": len(predictions), "reorders": len(all_reorders)}

    except Exception as exc:
        logger.exception("Predictive analysis failed: %s", exc)
        raise self.retry(exc=exc, countdown=60)


@shared_task
def ingest_telemetry_task(vehicle_id: str, events: list):
    """
    Bulk ingest telemetry events from telematics provider.
    Called by Samsara/Geotab webhook handlers.
    """
    from apps.fleet.models import Vehicle, TelemetryEvent
    from django.utils.dateparse import parse_datetime
    from core.events.models import EventPublisher

    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
    except Vehicle.DoesNotExist:
        return

    critical_codes = {"P0300", "P0562", "U0100", "P0420"}
    critical_found = []

    for e in events:
        te = TelemetryEvent.objects.create(
            vehicle=vehicle,
            code=e.get("code", ""),
            description=e.get("description", ""),
            payload=e,
            severity=e.get("severity", "info"),
            timestamp=parse_datetime(e.get("timestamp", "")) or __import__("django.utils.timezone", fromlist=["now"]).now(),
        )
        if te.code in critical_codes:
            critical_found.append(te.code)

    if critical_found:
        EventPublisher.publish(
            event_type="vehicle.fault_detected",
            aggregate_type="Vehicle",
            aggregate_id=str(vehicle.id),
            payload={"vehicle_id": str(vehicle.id), "fault_codes": critical_found},
            organization_id=vehicle.organization_id,
        )

    # Update odometer if present
    latest_odometer = max((e.get("odometer", 0) for e in events), default=0)
    if latest_odometer > vehicle.odometer:
        vehicle.odometer = latest_odometer
        vehicle.save(update_fields=["odometer"])
