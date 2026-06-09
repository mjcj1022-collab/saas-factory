from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q

from .models import KnowledgeDocument, RFPRequest, RFPSection, GeneratedResponse
from . import tasks as rfp_tasks
from .serializers import (
    KnowledgeDocumentSerializer, RFPRequestSerializer,
    RFPListSerializer, RFPSectionSerializer, GeneratedResponseSerializer,
)


class KnowledgeDocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = KnowledgeDocumentSerializer

    def get_queryset(self):
        return KnowledgeDocument.objects.filter(
            organization_id=self.request.user.organization_id
        ).order_by("-uploaded_at")

    def perform_create(self, serializer):
        doc = serializer.save()
        # Queue embedding generation
        rfp_tasks.create_embeddings_task.delay(str(doc.id))


class RFPRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return RFPListSerializer
        return RFPRequestSerializer

    def get_queryset(self):
        return RFPRequest.objects.filter(
            organization_id=self.request.user.organization_id
        ).order_by("-created_at")

    def perform_create(self, serializer):
        rfp = serializer.save()
        rfp_tasks.parse_rfp_task.delay(str(rfp.id))

    @action(detail=True, methods=["post"])
    def generate(self, request, pk=None):
        """Re-trigger AI generation for an RFP."""
        rfp = self.get_object()
        # tasks imported at module level
        rfp.status = "generating"
        rfp.save(update_fields=["status"])
        rfp_tasks.generate_responses_task.delay(str(rfp.id))
        return Response({"status": "generation queued"})

    @action(detail=True, methods=["post"])
    def export(self, request, pk=None):
        """Export RFP responses to DOCX."""
        rfp = self.get_object()
        fmt = request.data.get("format", "docx")
        rfp_tasks.export_rfp_task.delay(str(rfp.id), fmt)
        return Response({"status": f"export to {fmt} queued"})

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        rfp = self.get_object()
        sections = rfp.sections.all()
        total = sections.count()
        reviewed = sections.filter(response__reviewed=True).count()
        approved = sections.filter(response__approved=True).count()
        needs_review = sections.filter(response__confidence_score__lt=0.5).count()
        return Response({
            "total_sections": total,
            "reviewed": reviewed,
            "approved": approved,
            "needs_review": needs_review,
            "completion_pct": round(approved / total * 100, 1) if total else 0,
        })


class GeneratedResponseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GeneratedResponseSerializer

    def get_queryset(self):
        return GeneratedResponse.objects.filter(
            section__rfp__organization_id=self.request.user.organization_id
        ).select_related("section", "section__rfp")

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        response = self.get_object()
        response.approved = True
        response.reviewed = True
        response.reviewer_notes = request.data.get("notes", "")
        response.save(update_fields=["approved", "reviewed", "reviewer_notes"])
        return Response(GeneratedResponseSerializer(response).data)

    @action(detail=True, methods=["post"])
    def request_revision(self, request, pk=None):
        response = self.get_object()
        response.approved = False
        response.reviewed = True
        response.reviewer_notes = request.data.get("notes", "")
        response.save(update_fields=["approved", "reviewed", "reviewer_notes"])
        return Response(GeneratedResponseSerializer(response).data)
