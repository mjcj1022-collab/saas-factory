from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KnowledgeDocumentViewSet, RFPRequestViewSet, GeneratedResponseViewSet

router = DefaultRouter()
router.register("knowledge", KnowledgeDocumentViewSet, basename="knowledge")
router.register("requests", RFPRequestViewSet, basename="rfp")
router.register("responses", GeneratedResponseViewSet, basename="rfp-response")

urlpatterns = [path("", include(router.urls))]
