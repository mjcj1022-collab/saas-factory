from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import *  # uncomment after adding viewsets

router = DefaultRouter()
# router.register("...", SomeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
