from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmViewSet, ProduceViewSet, HarvestLogViewSet, StoreViewSet, DeliveryRouteViewSet, DeliveryViewSet

router = DefaultRouter()
router.register('farms', FarmViewSet, basename='farm')
router.register('produces', ProduceViewSet, basename='produce')
router.register('harvestlogs', HarvestLogViewSet, basename='harvestlog')
router.register('stores', StoreViewSet, basename='store')
router.register('deliveryroutes', DeliveryRouteViewSet, basename='deliveryroute')
router.register('deliverys', DeliveryViewSet, basename='delivery')

urlpatterns = [path("", include(router.urls))]
