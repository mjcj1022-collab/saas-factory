from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VenueViewSet, RoomViewSet, VenueBookingViewSet, VendorAssignmentViewSet, VenueInvoiceViewSet

router = DefaultRouter()
router.register('venues', VenueViewSet, basename='venue')
router.register('rooms', RoomViewSet, basename='room')
router.register('venuebookings', VenueBookingViewSet, basename='venuebooking')
router.register('vendorassignments', VendorAssignmentViewSet, basename='vendorassignment')
router.register('venueinvoices', VenueInvoiceViewSet, basename='venueinvoice')

urlpatterns = [path("", include(router.urls))]
