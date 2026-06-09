from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet, InvoiceViewSet

router = DefaultRouter()
router.register("subscriptions", SubscriptionViewSet, basename="subscription")
router.register("invoices", InvoiceViewSet, basename="invoice")

urlpatterns = [path("", include(router.urls))]
