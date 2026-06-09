from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import RentalProperty, Reservation, GuestThread, CleaningJob
from .serializers import RentalPropertySerializer, ReservationSerializer, GuestThreadSerializer, CleaningJobSerializer

class RentalPropertyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RentalPropertySerializer

    def get_queryset(self):
        return RentalProperty.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class GuestThreadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GuestThreadSerializer

    def get_queryset(self):
        return GuestThread.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()

class CleaningJobViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CleaningJobSerializer

    def get_queryset(self):
        return CleaningJob.objects.filter(organization_id=self.request.user.organization_id).order_by('-id')

    def perform_create(self, serializer):
        org_id = self.request.user.organization_id
        serializer.save()
