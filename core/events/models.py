import uuid
from django.db import models


EVENT_TYPES = [
    # RFP
    "rfp.uploaded",
    "rfp.sections_extracted",
    "rfp.responses_generated",
    "rfp.exported",
    # Construction
    "drawing.uploaded",
    "drawing.revision_detected",
    "drawing.impact_analyzed",
    # Franchise
    "franchise.application_submitted",
    "franchise.milestone_completed",
    "franchise.training_completed",
    # Fleet
    "vehicle.fault_detected",
    "vehicle.work_order_created",
    "vehicle.repair_completed",
    # Solar
    "solar.project_created",
    "solar.permit_submitted",
    "solar.permit_approved",
    # Hospitality
    "booking.confirmed",
    "booking.checkin",
    "booking.checkout",
    "lock.code_generated",
    # Venue
    "venue.booking_created",
    "venue.invoice_generated",
    # Sourcing
    "supplier.quote_received",
    "production.run_started",
    "shipment.dispatched",
    # Agency
    "asset.uploaded",
    "asset.approved",
    "invoice.triggered",
    # Food
    "harvest.logged",
    "route.generated",
    "delivery.completed",
    # Platform
    "invoice.paid",
    "subscription.created",
    "subscription.canceled",
    "workflow.completed",
    "notification.sent",
]


class DomainEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    event_type = models.CharField(max_length=200, db_index=True)
    aggregate_type = models.CharField(max_length=100)
    aggregate_id = models.CharField(max_length=100)
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    processed = models.BooleanField(default=False, db_index=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(blank=True)

    class Meta:
        db_table = "domain_events"
        ordering = ["-created_at"]


class EventPublisher:
    """
    Publish domain events. In production, swap storage backend
    for Redis Streams / Kafka by overriding _dispatch().
    """

    @staticmethod
    def publish(
        event_type: str,
        aggregate_type: str,
        aggregate_id: str,
        payload: dict,
        organization_id=None,
    ) -> DomainEvent:
        event = DomainEvent.objects.create(
            event_type=event_type,
            aggregate_type=aggregate_type,
            aggregate_id=str(aggregate_id),
            payload=payload,
            organization_id=organization_id or uuid.uuid4(),
        )
        EventPublisher._dispatch(event)
        return event

    @staticmethod
    def _dispatch(event: DomainEvent):
        """Hook for Redis Streams / Kafka dispatch."""
        from core.events.router import EventRouter
        EventRouter.route(event)


class EventSubscription(models.Model):
    """Registry of handler classes subscribed to event types."""
    event_type = models.CharField(max_length=200)
    handler_path = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "event_subscriptions"


class EventRouter:
    _registry: dict = {}

    @classmethod
    def register(cls, event_type: str, handler_callable):
        cls._registry.setdefault(event_type, []).append(handler_callable)

    @classmethod
    def route(cls, event: DomainEvent):
        handlers = cls._registry.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as exc:
                event.error = str(exc)
                event.save(update_fields=["error"])
