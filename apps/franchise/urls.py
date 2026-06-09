from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FranchiseBrandViewSet, FranchiseeViewSet, FranchiseLocationViewSet, MilestoneViewSet

router = DefaultRouter()
router.register("brands", FranchiseBrandViewSet, basename="brand")
router.register("franchisees", FranchiseeViewSet, basename="franchisee")
router.register("locations", FranchiseLocationViewSet, basename="location")
router.register("milestones", MilestoneViewSet, basename="milestone")

urlpatterns = [path("", include(router.urls))]
