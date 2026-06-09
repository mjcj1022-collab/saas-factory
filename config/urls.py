from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("rest_framework.urls")),
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
    path("api/platform/events/", include("core.events.urls")),
    path("api/platform/workflows/", include("core.workflows.urls")),
    path("api/platform/billing/", include("core.billing.urls")),
    path("api/platform/notifications/", include("core.notifications.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
