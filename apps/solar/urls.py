from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, RoofPlaneViewSet, SolarArrayViewSet, PermitViewSet, SetbackValidationViewSet, InspectionViewSet

router = DefaultRouter()
router.register('propertys', PropertyViewSet, basename='property')
router.register('roofplanes', RoofPlaneViewSet, basename='roofplane')
router.register('solararrays', SolarArrayViewSet, basename='solararray')
router.register('permits', PermitViewSet, basename='permit')
router.register('setbackvalidations', SetbackValidationViewSet, basename='setbackvalidation')
router.register('inspections', InspectionViewSet, basename='inspection')

urlpatterns = [path("", include(router.urls))]
