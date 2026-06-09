from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, AgencyProjectViewSet, AssetViewSet, AssetVersionViewSet, ApprovalRequestViewSet, AgencyInvoiceViewSet

router = DefaultRouter()
router.register('clients', ClientViewSet, basename='client')
router.register('agencyprojects', AgencyProjectViewSet, basename='agencyproject')
router.register('assets', AssetViewSet, basename='asset')
router.register('assetversions', AssetVersionViewSet, basename='assetversion')
router.register('approvalrequests', ApprovalRequestViewSet, basename='approvalrequest')
router.register('agencyinvoices', AgencyInvoiceViewSet, basename='agencyinvoice')

urlpatterns = [path("", include(router.urls))]
