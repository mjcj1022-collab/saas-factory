"""
Stripe webhook endpoint.
Add to urls.py: path("webhooks/stripe/", stripe_webhook)
"""
import json
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def stripe_webhook(request):
    import stripe
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    _handle_event(event)
    return HttpResponse(status=200)


def _handle_event(event):
    from core.billing.models import Subscription, Invoice
    from core.events.models import EventPublisher

    etype = event["type"]
    data = event["data"]["object"]

    if etype == "customer.subscription.updated":
        org_id = data.get("metadata", {}).get("organization_id")
        if org_id:
            Subscription.objects.filter(
                stripe_subscription_id=data["id"]
            ).update(
                status=data["status"],
                plan=_price_to_plan(data),
            )
            EventPublisher.publish(
                event_type="subscription.updated",
                aggregate_type="Subscription",
                aggregate_id=data["id"],
                payload={"status": data["status"]},
                organization_id=org_id,
            )

    elif etype == "invoice.paid":
        org_id = data.get("metadata", {}).get("organization_id")
        if org_id:
            from django.utils import timezone
            Invoice.objects.update_or_create(
                stripe_invoice_id=data["id"],
                defaults={
                    "organization_id": org_id,
                    "amount_cents": data["amount_paid"],
                    "currency": data["currency"],
                    "status": "paid",
                    "paid_at": timezone.now(),
                },
            )
            EventPublisher.publish(
                event_type="invoice.paid",
                aggregate_type="Invoice",
                aggregate_id=data["id"],
                payload={"amount_cents": data["amount_paid"]},
                organization_id=org_id,
            )

    elif etype == "customer.subscription.deleted":
        Subscription.objects.filter(
            stripe_subscription_id=data["id"]
        ).update(status="canceled")


def _price_to_plan(subscription_data) -> str:
    try:
        price_id = subscription_data["items"]["data"][0]["price"]["id"]
        if "growth" in price_id:
            return "growth"
        if "enterprise" in price_id:
            return "enterprise"
    except (KeyError, IndexError):
        pass
    return "starter"
