from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from django.utils import timezone


def health_check(request):
    return JsonResponse({
        "status": "ok",
        "time": timezone.now().isoformat(),
        "version": "1.0.0",
    })


urlpatterns = [
    # Health check — used by Railway/Render
    path("health/", health_check),
    # Admin
    path("admin/", admin.site.urls),
    # Auth
    path("api/auth/", include("core.organizations.urls")),
    path("api/drf-auth/", include("rest_framework.urls")),
    # Platform
    path("api/platform/events/", include("core.events.urls")),
    path("api/platform/workflows/", include("core.workflows.urls")),
    path("api/platform/billing/", include("core.billing.urls")),
    path("api/platform/notifications/", include("core.notifications.urls")),
    # Stripe webhook
    path("webhooks/stripe/", include("core.billing.webhook_urls")),
    # Vertical apps
    path("api/rfp/", include("apps.rfp.urls")),
    path("api/construction/", include("apps.construction.urls")),
    path("api/franchise/", include("apps.franchise.urls")),
    path("api/fleet/", include("apps.fleet.urls")),
    path("api/solar/", include("apps.solar.urls")),
    path("api/hospitality/", include("apps.hospitality.urls")),
    path("api/venue/", include("apps.venue.urls")),
    path("api/sourcing/", include("apps.sourcing.urls")),
    path("api/agency/", include("apps.agency.urls")),
    path("api/food/", include("apps.food.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
