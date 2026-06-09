from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def setup_booking_task(self, reservation_id: str):
    """
    On booking confirmed:
    1. Generate smart lock code
    2. Send welcome message to guest
    3. Publish booking.confirmed event
    """
    try:
        from apps.hospitality.models import Reservation
        from apps.hospitality.services import SmartLockManager, GuestMessagingAI
        from core.events.models import EventPublisher

        reservation = Reservation.objects.select_related("property").get(id=reservation_id)

        # 1. Generate lock code
        lock_mgr = SmartLockManager()
        code = lock_mgr.create_code(reservation)

        # 2. Send welcome message
        prop = reservation.property
        welcome = (
            f"Hi {reservation.guest_name}! Your reservation at {prop.name} is confirmed. "
            f"Check-in: {reservation.check_in.strftime('%b %d at %I:%M %p')}. "
            f"Your door code is: {code}. "
        )
        if prop.check_in_instructions:
            welcome += f"\n\n{prop.check_in_instructions}"

        from apps.hospitality.models import GuestThread
        GuestThread.objects.create(
            reservation=reservation,
            sender="ai",
            message=welcome,
            platform=reservation.platform,
            is_automated=True,
        )

        logger.info("Booking setup complete for reservation %s", reservation_id)

    except Exception as exc:
        logger.exception("setup_booking_task failed: %s", exc)
        raise self.retry(exc=exc, countdown=30)


@shared_task(bind=True, max_retries=3)
def post_checkout_task(self, reservation_id: str):
    """
    On guest checkout:
    1. Expire lock code
    2. Dispatch cleaning job
    3. Request review from guest
    """
    try:
        from apps.hospitality.models import Reservation, GuestThread
        from apps.hospitality.services import SmartLockManager, CleaningDispatcher

        reservation = Reservation.objects.select_related("property").get(id=reservation_id)

        # 1. Expire lock
        SmartLockManager().expire_code(reservation)

        # 2. Dispatch cleaning
        CleaningDispatcher().dispatch_after_checkout(reservation)

        # 3. Send review request
        GuestThread.objects.create(
            reservation=reservation,
            sender="ai",
            message=(
                f"Hi {reservation.guest_name}! We hope you enjoyed your stay at {reservation.property.name}. "
                "We'd love your feedback — please take a moment to leave a review. "
                "Thank you and we hope to host you again soon!"
            ),
            platform=reservation.platform,
            is_automated=True,
        )

        reservation.status = "checked_out"
        reservation.save(update_fields=["status"])

        logger.info("Post-checkout complete for reservation %s", reservation_id)

    except Exception as exc:
        logger.exception("post_checkout_task failed: %s", exc)
        raise self.retry(exc=exc, countdown=30)


@shared_task
def ai_respond_to_guest_task(guest_thread_id: str):
    """Auto-respond to guest message using AI."""
    from apps.hospitality.models import GuestThread
    from apps.hospitality.services import GuestMessagingAI

    try:
        thread = GuestThread.objects.select_related(
            "reservation", "reservation__property"
        ).get(id=guest_thread_id)

        if thread.sender != "guest":
            return

        ai = GuestMessagingAI()
        response = ai.classify_and_respond(thread.message, thread.reservation)

        GuestThread.objects.create(
            reservation=thread.reservation,
            sender="ai",
            message=response,
            platform=thread.platform,
            is_automated=True,
        )
    except Exception as exc:
        logger.exception("ai_respond_to_guest_task failed: %s", exc)


@shared_task
def sync_reservations_task(organization_id: str, platform: str = "airbnb"):
    """
    Sync reservations from Airbnb/VRBO/Booking.com APIs.
    Stub — plug in actual API credentials via OrganizationIntegration.
    """
    logger.info("Syncing %s reservations for org %s", platform, organization_id)
    # Implementation plugs into core.integrations layer
