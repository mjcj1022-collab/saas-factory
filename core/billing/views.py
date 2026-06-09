from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Subscription, Invoice, UsageRecord
from rest_framework import serializers


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            "id", "organization_id", "stripe_customer_id",
            "plan", "status", "current_period_start",
            "current_period_end", "created_at",
        ]
        read_only_fields = ["id", "created_at", "stripe_customer_id"]


class InvoiceSerializer(serializers.ModelSerializer):
    amount_dollars = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ["id", "organization_id", "amount_cents", "amount_dollars", "currency", "status", "paid_at", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_amount_dollars(self, obj):
        return round(obj.amount_cents / 100, 2)


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(organization_id=self.request.user.organization_id)

    @action(detail=False, methods=["get"])
    def current(self, request):
        sub = Subscription.objects.filter(
            organization_id=request.user.organization_id,
            status__in=["active", "trialing"],
        ).order_by("-created_at").first()
        if not sub:
            return Response({"plan": "free", "status": "none"})
        return Response(SubscriptionSerializer(sub).data)

    @action(detail=False, methods=["post"])
    def create_checkout(self, request):
        """Create Stripe checkout session — returns URL."""
        plan = request.data.get("plan", "starter")
        PLAN_PRICES = {
            "starter": "price_starter",
            "growth": "price_growth",
            "enterprise": "price_enterprise",
        }
        try:
            import stripe, os
            stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
            session = stripe.checkout.Session.create(
                mode="subscription",
                line_items=[{"price": PLAN_PRICES.get(plan, "price_starter"), "quantity": 1}],
                success_url=request.data.get("success_url", "http://localhost:3000/billing?success=1"),
                cancel_url=request.data.get("cancel_url", "http://localhost:3000/billing"),
                metadata={"organization_id": str(request.user.organization_id)},
            )
            return Response({"checkout_url": session.url})
        except Exception as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.filter(
            organization_id=self.request.user.organization_id
        ).order_by("-created_at")
