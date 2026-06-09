from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Farm, Produce, HarvestLog, Store, DeliveryRoute, Delivery
from .serializers import FarmSerializer, ProduceSerializer, HarvestLogSerializer, StoreSerializer, DeliveryRouteSerializer, DeliverySerializer

class FarmViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FarmSerializer

    def get_queryset(self):
        return Farm.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class ProduceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProduceSerializer

    def get_queryset(self):
        return Produce.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class HarvestLogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HarvestLogSerializer

    def get_queryset(self):
        return HarvestLog.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class StoreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class DeliveryRouteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryRouteSerializer

    def get_queryset(self):
        return DeliveryRoute.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class DeliveryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializer

    def get_queryset(self):
        return Delivery.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()
