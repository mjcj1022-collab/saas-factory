from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Project, Drawing, RevisionAnalysis, TradePackage, PunchItem, DailyReport
from .serializers import (
    ProjectSerializer, DrawingSerializer, RevisionAnalysisSerializer,
    TradePackageSerializer, PunchItemSerializer, DailyReportSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(organization_id=self.request.user.organization_id)


class DrawingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DrawingSerializer

    def get_queryset(self):
        return Drawing.objects.filter(
            project__organization_id=self.request.user.organization_id
        ).order_by("-uploaded_at")

    def perform_create(self, serializer):
        drawing = serializer.save()
        # Detect revision if same drawing number exists
        prev = Drawing.objects.filter(
            project=drawing.project,
            drawing_number=drawing.drawing_number,
        ).exclude(id=drawing.id).order_by("-uploaded_at").first()
        if prev:
            from .tasks import analyze_revision_task
            analyze_revision_task.delay(str(prev.id), str(drawing.id))


class RevisionAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RevisionAnalysisSerializer

    def get_queryset(self):
        return RevisionAnalysis.objects.filter(
            new_drawing__project__organization_id=self.request.user.organization_id
        ).order_by("-analyzed_at")


class TradePackageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TradePackageSerializer

    def get_queryset(self):
        return TradePackage.objects.filter(
            project__organization_id=self.request.user.organization_id
        )


class PunchItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PunchItemSerializer

    def get_queryset(self):
        return PunchItem.objects.filter(
            project__organization_id=self.request.user.organization_id
        ).order_by("-created_at")


class DailyReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DailyReportSerializer

    def get_queryset(self):
        return DailyReport.objects.filter(
            project__organization_id=self.request.user.organization_id
        ).order_by("-report_date")
