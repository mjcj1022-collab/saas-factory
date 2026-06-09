from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, NotificationPreferenceViewSet

router = DefaultRouter()
router.register("", NotificationViewSet, basename="notification")
router.register("preferences", NotificationPreferenceViewSet, basename="notif-pref")
urlpatterns = [path("", include(router.urls))]
