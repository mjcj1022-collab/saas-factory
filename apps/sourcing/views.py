from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Supplier, Product, SupplierQuote, ProductionRun, Shipment
from .serializers import SupplierSerializer, ProductSerializer, SupplierQuoteSerializer, ProductionRunSerializer, ShipmentSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SupplierSerializer

    def get_queryset(self):
        return Supplier.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class SupplierQuoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SupplierQuoteSerializer

    def get_queryset(self):
        return SupplierQuote.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class ProductionRunViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductionRunSerializer

    def get_queryset(self):
        return ProductionRun.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class ShipmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        return Shipment.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()
