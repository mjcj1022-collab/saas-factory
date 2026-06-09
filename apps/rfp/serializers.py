from rest_framework import serializers
from .models import (
    KnowledgeDocument, KnowledgeChunk, RFPRequest,
    RFPSection, GeneratedResponse, ComplianceGap,
)


class KnowledgeChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeChunk
        fields = ["id", "chunk_text", "sequence", "metadata"]
        read_only_fields = ["id"]


class KnowledgeDocumentSerializer(serializers.ModelSerializer):
    chunk_count = serializers.SerializerMethodField()

    class Meta:
        model = KnowledgeDocument
        fields = ["id", "title", "file", "doc_type", "tags", "uploaded_at", "chunk_count"]
        read_only_fields = ["id", "uploaded_at"]

    def get_chunk_count(self, obj):
        return obj.chunks.count()

    def create(self, validated_data):
        validated_data["organization_id"] = self.context["request"].user.organization_id
        return super().create(validated_data)


class ComplianceGapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceGap
        fields = ["id", "framework", "issue", "recommendation", "severity"]


class GeneratedResponseSerializer(serializers.ModelSerializer):
    compliance_gaps = ComplianceGapSerializer(many=True, read_only=True)

    class Meta:
        model = GeneratedResponse
        fields = [
            "id", "answer", "confidence_score", "source_chunks",
            "reviewed", "approved", "reviewer_notes",
            "generated_at", "updated_at", "compliance_gaps",
        ]
        read_only_fields = ["id", "generated_at", "updated_at", "compliance_gaps"]


class RFPSectionSerializer(serializers.ModelSerializer):
    response = GeneratedResponseSerializer(read_only=True)

    class Meta:
        model = RFPSection
        fields = ["id", "heading", "question", "category", "sequence", "is_required", "response"]
        read_only_fields = ["id"]


class RFPRequestSerializer(serializers.ModelSerializer):
    sections = RFPSectionSerializer(many=True, read_only=True)
    section_count = serializers.SerializerMethodField()
    approved_count = serializers.SerializerMethodField()

    class Meta:
        model = RFPRequest
        fields = [
            "id", "title", "original_file", "issuer", "due_date",
            "status", "created_at", "updated_at",
            "section_count", "approved_count", "sections",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]

    def get_section_count(self, obj):
        return obj.sections.count()

    def get_approved_count(self, obj):
        return obj.sections.filter(response__approved=True).count()

    def create(self, validated_data):
        validated_data["organization_id"] = self.context["request"].user.organization_id
        return super().create(validated_data)


class RFPListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views — no nested sections."""
    section_count = serializers.SerializerMethodField()
    approved_count = serializers.SerializerMethodField()

    class Meta:
        model = RFPRequest
        fields = ["id", "title", "issuer", "due_date", "status", "created_at", "section_count", "approved_count"]

    def get_section_count(self, obj):
        return obj.sections.count()

    def get_approved_count(self, obj):
        return obj.sections.filter(response__approved=True).count()
