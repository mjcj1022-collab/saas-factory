from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import FranchiseBrand, Franchisee, FranchiseLocation, Milestone, TrainingModule
from .serializers import (
    FranchiseBrandSerializer, FranchiseeSerializer, FranchiseLocationSerializer,
    MilestoneSerializer, TrainingModuleSerializer,
)


class FranchiseBrandViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FranchiseBrandSerializer

    def get_queryset(self):
        return FranchiseBrand.objects.filter(organization_id=self.request.user.organization_id)


class FranchiseeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FranchiseeSerializer

    def get_queryset(self):
        return Franchisee.objects.filter(brand__organization_id=self.request.user.organization_id)


class FranchiseLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FranchiseLocationSerializer

    def get_queryset(self):
        return FranchiseLocation.objects.filter(
            franchisee__brand__organization_id=self.request.user.organization_id
        )

    @action(detail=False, methods=["get"])
    def pipeline(self, request):
        """Kanban-style pipeline grouped by launch_status."""
        locations = self.get_queryset()
        stages = {}
        for loc in locations:
            stage = loc.launch_status
            if stage not in stages:
                stages[stage] = []
            stages[stage].append(FranchiseLocationSerializer(loc).data)
        return Response(stages)

    @action(detail=True, methods=["post"])
    def advance_stage(self, request, pk=None):
        STAGES = ["pipeline", "site_selection", "lease_negotiation", "construction", "training", "pre_open", "open"]
        loc = self.get_object()
        try:
            idx = STAGES.index(loc.launch_status)
            if idx < len(STAGES) - 1:
                loc.launch_status = STAGES[idx + 1]
                loc.save(update_fields=["launch_status"])
        except ValueError:
            pass
        return Response(FranchiseLocationSerializer(loc).data)


class MilestoneViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MilestoneSerializer

    def get_queryset(self):
        return Milestone.objects.filter(
            location__franchisee__brand__organization_id=self.request.user.organization_id
        )

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        from django.utils import timezone
        milestone = self.get_object()
        milestone.completed = True
        milestone.completed_at = timezone.now()
        milestone.save(update_fields=["completed", "completed_at"])
        return Response(MilestoneSerializer(milestone).data)
