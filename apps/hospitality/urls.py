from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RentalPropertyViewSet, ReservationViewSet, GuestThreadViewSet, CleaningJobViewSet

router = DefaultRouter()
router.register('rentalpropertys', RentalPropertyViewSet, basename='rentalproperty')
router.register('reservations', ReservationViewSet, basename='reservation')
router.register('guestthreads', GuestThreadViewSet, basename='guestthread')
router.register('cleaningjobs', CleaningJobViewSet, basename='cleaningjob')

urlpatterns = [path("", include(router.urls))]
