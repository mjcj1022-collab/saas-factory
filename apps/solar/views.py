from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Property, RoofPlane, SolarArray, Permit, SetbackValidation, Inspection
from .serializers import PropertySerializer, RoofPlaneSerializer, SolarArraySerializer, PermitSerializer, SetbackValidationSerializer, InspectionSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer

    def get_queryset(self):
        return Property.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class RoofPlaneViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RoofPlaneSerializer

    def get_queryset(self):
        return RoofPlane.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class SolarArrayViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SolarArraySerializer

    def get_queryset(self):
        return SolarArray.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class PermitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PermitSerializer

    def get_queryset(self):
        return Permit.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class SetbackValidationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SetbackValidationSerializer

    def get_queryset(self):
        return SetbackValidation.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class InspectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InspectionSerializer

    def get_queryset(self):
        return Inspection.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()
