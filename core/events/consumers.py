"""
Event consumers — register handlers for all domain event types.
Imported once at app startup via AppConfig.ready().

Each handler receives a DomainEvent instance and performs side effects:
  - Trigger workflows
  - Send notifications
  - Kick off Celery tasks
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)


def register_all():
    """Call from AppConfig.ready() to wire up all consumers."""
    from core.events.models import EventRouter

    # ── RFP ──────────────────────────────────────────────────────────────────
    EventRouter.register("rfp.uploaded", on_rfp_uploaded)
    EventRouter.register("rfp.responses_generated", on_rfp_responses_generated)

    # ── Construction ─────────────────────────────────────────────────────────
    EventRouter.register("drawing.revision_detected", on_revision_detected)

    # ── Fleet ─────────────────────────────────────────────────────────────────
    EventRouter.register("vehicle.fault_detected", on_fault_detected)
    EventRouter.register("vehicle.work_order_created", on_work_order_created)

    # ── Hospitality ───────────────────────────────────────────────────────────
    EventRouter.register("booking.confirmed", on_booking_confirmed)
    EventRouter.register("booking.checkout", on_booking_checkout)

    # ── Franchise ────────────────────────────────────────────────────────────
    EventRouter.register("franchise.milestone_completed", on_milestone_completed)

    # ── Billing ───────────────────────────────────────────────────────────────
    EventRouter.register("invoice.paid", on_invoice_paid)

    # ── All events → workflow engine ──────────────────────────────────────────
    from core.events.models import EVENT_TYPES
    for etype in EVENT_TYPES:
        EventRouter.register(etype, run_workflows)

    logger.info("Event consumers registered (%d event types)", len(EVENT_TYPES))


# ─── RFP Consumers ───────────────────────────────────────────────────────────

def on_rfp_uploaded(event):
    from apps.rfp.tasks import parse_rfp_task
    rfp_id = event.payload.get("rfp_id")
    if rfp_id:
        parse_rfp_task.delay(rfp_id)


def on_rfp_responses_generated(event):
    """Notify the submitting user that their RFP is ready for review."""
    rfp_id = event.payload.get("rfp_id")
    if not rfp_id:
        return
    _notify(
        organization_id=event.organization_id,
        channel="email",
        subject="Your RFP responses are ready for review",
        message=f"AI has generated responses for RFP {rfp_id}. Log in to review and approve.",
    )


# ─── Construction Consumers ──────────────────────────────────────────────────

def on_revision_detected(event):
    affected_trades = event.payload.get("affected_trades", [])
    if not affected_trades:
        return
    _notify(
        organization_id=event.organization_id,
        channel="email",
        subject="Drawing revision detected — trade impact identified",
        message=f"Affected trades: {', '.join(affected_trades)}. Review material impacts in the Construction module.",
    )


# ─── Fleet Consumers ─────────────────────────────────────────────────────────

def on_fault_detected(event):
    from apps.fleet.tasks import run_predictive_analysis_task
    vehicle_id = event.payload.get("vehicle_id")
    if vehicle_id:
        run_predictive_analysis_task.delay(vehicle_id)


def on_work_order_created(event):
    _notify(
        organization_id=event.organization_id,
        channel="slack",
        subject="",
        message=f"New work order created: {event.payload.get('description', 'See fleet dashboard')}",
    )


# ─── Hospitality Consumers ───────────────────────────────────────────────────

def on_booking_confirmed(event):
    """Generate lock code + send welcome message on booking confirmation."""
    from apps.hospitality.tasks import setup_booking_task
    reservation_id = event.payload.get("reservation_id")
    if reservation_id:
        setup_booking_task.delay(reservation_id)


def on_booking_checkout(event):
    """Expire lock code + dispatch cleaning on checkout."""
    from apps.hospitality.tasks import post_checkout_task
    reservation_id = event.payload.get("reservation_id")
    if reservation_id:
        post_checkout_task.delay(reservation_id)


# ─── Franchise Consumers ─────────────────────────────────────────────────────

def on_milestone_completed(event):
    milestone_title = event.payload.get("milestone_title", "Milestone")
    location_id = event.payload.get("location_id")
    _notify(
        organization_id=event.organization_id,
        channel="email",
        subject=f"Milestone completed: {milestone_title}",
        message=f"Location {location_id} completed milestone: {milestone_title}",
    )


# ─── Billing Consumers ───────────────────────────────────────────────────────

def on_invoice_paid(event):
    amount = event.payload.get("amount_cents", 0)
    _notify(
        organization_id=event.organization_id,
        channel="email",
        subject="Payment received",
        message=f"Your payment of ${amount/100:.2f} has been received. Thank you.",
    )


# ─── Workflow Trigger ─────────────────────────────────────────────────────────

def run_workflows(event):
    from core.workflows.executor import WorkflowExecutor
    try:
        WorkflowExecutor.run_for_event(event)
    except Exception as exc:
        logger.exception("Workflow execution failed for event %s: %s", event.event_type, exc)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _notify(organization_id, channel: str, subject: str, message: str, recipient: str = "admin"):
    from core.notifications.models import Notification
    try:
        Notification.objects.create(
            organization_id=organization_id,
            channel=channel,
            recipient=recipient,
            subject=subject,
            message=message,
        )
    except Exception as exc:
        logger.warning("Failed to create notification: %s", exc)
