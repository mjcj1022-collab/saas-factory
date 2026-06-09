"""
Hospitality — AI guest messaging + smart lock automation.
"""
from __future__ import annotations
from datetime import timedelta


COMMON_QUESTIONS = {
    "wifi": "wifi_password",
    "password": "wifi_password",
    "internet": "wifi_password",
    "check in": "check_in_instructions",
    "checkin": "check_in_instructions",
    "check-in": "check_in_instructions",
    "check out": None,
    "checkout": None,
    "parking": None,
    "rules": "house_rules",
}


class GuestMessagingAI:
    """
    Auto-responds to guest messages using property data + AI fallback.
    """

    def classify_and_respond(self, message: str, reservation) -> str:
        msg_lower = message.lower()
        prop = reservation.property

        for keyword, field in COMMON_QUESTIONS.items():
            if keyword in msg_lower and field:
                value = getattr(prop, field, None)
                if value:
                    return self._format_response(keyword, value, reservation)

        # AI fallback
        return self._ai_respond(message, reservation)

    def _format_response(self, topic: str, value: str, reservation) -> str:
        templates = {
            "wifi_password": f"Hi {reservation.guest_name}! Your WiFi password is: **{value}**. Let me know if you need anything else!",
            "check_in_instructions": f"Hi {reservation.guest_name}! Here are your check-in instructions:\n\n{value}",
            "house_rules": f"Hi {reservation.guest_name}! Our house rules:\n\n{value}",
        }
        return templates.get(topic, value)

    def _ai_respond(self, message: str, reservation) -> str:
        from core.ai.services import AIRouter
        prop = reservation.property
        context = f"""
Property: {prop.name}
Address: {prop.address}
Check-in instructions: {prop.check_in_instructions}
House rules: {prop.house_rules}
Guest: {reservation.guest_name}
Check-in: {reservation.check_in}
Check-out: {reservation.check_out}
"""
        system = (
            "You are a helpful short-term rental host assistant. "
            "Answer guest questions using the provided property info. "
            "Be friendly, brief, and helpful. Never make up info not in the context."
        )
        prompt = f"PROPERTY INFO:\n{context}\n\nGUEST MESSAGE:\n{message}"
        return AIRouter.generate("guest_message", prompt, system=system, max_tokens=500)


class SmartLockManager:
    """
    Manages lock code lifecycle for reservations.
    Supports: August, Schlage, Yale, Kwikset via provider abstraction.
    """

    def create_code(self, reservation) -> str:
        import random, string
        code = "".join(random.choices(string.digits, k=6))

        from apps.hospitality.models import SmartLockCode
        SmartLockCode.objects.update_or_create(
            reservation=reservation,
            defaults={
                "code": code,
                "lock_provider": "generic",
                "valid_from": reservation.check_in,
                "valid_until": reservation.check_out,
                "created": True,
            },
        )
        return code

    def expire_code(self, reservation):
        from apps.hospitality.models import SmartLockCode
        try:
            lock = reservation.lock_code
            lock.created = False
            lock.save(update_fields=["created"])
        except SmartLockCode.DoesNotExist:
            pass


class CleaningDispatcher:
    """
    Auto-creates cleaning jobs on checkout.
    """

    def dispatch_after_checkout(self, reservation):
        from apps.hospitality.models import CleaningJob
        checkout_time = reservation.check_out
        scheduled = checkout_time + timedelta(hours=1)

        CleaningJob.objects.create(
            property=reservation.property,
            reservation=reservation,
            scheduled_time=scheduled,
            checklist=[
                "Strip all beds",
                "Replace linens",
                "Clean bathrooms",
                "Vacuum all rooms",
                "Mop kitchen floor",
                "Restock toiletries",
                "Check for damages",
                "Take photos",
            ],
        )
