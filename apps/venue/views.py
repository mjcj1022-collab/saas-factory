from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Venue, Room, VenueBooking, VendorAssignment, VenueInvoice
from .serializers import VenueSerializer, RoomSerializer, VenueBookingSerializer, VendorAssignmentSerializer, VenueInvoiceSerializer

class VenueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VenueSerializer

    def get_queryset(self):
        return Venue.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class VenueBookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VenueBookingSerializer

    def get_queryset(self):
        return VenueBooking.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class VendorAssignmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorAssignmentSerializer

    def get_queryset(self):
        return VendorAssignment.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class VenueInvoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VenueInvoiceSerializer

    def get_queryset(self):
        return VenueInvoice.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()
