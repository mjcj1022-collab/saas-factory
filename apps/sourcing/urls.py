from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, ProductViewSet, SupplierQuoteViewSet, ProductionRunViewSet, ShipmentViewSet

router = DefaultRouter()
router.register('suppliers', SupplierViewSet, basename='supplier')
router.register('products', ProductViewSet, basename='product')
router.register('supplierquotes', SupplierQuoteViewSet, basename='supplierquote')
router.register('productionruns', ProductionRunViewSet, basename='productionrun')
router.register('shipments', ShipmentViewSet, basename='shipment')

urlpatterns = [path("", include(router.urls))]
