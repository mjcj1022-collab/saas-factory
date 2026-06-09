from django.contrib import admin
from .models import KnowledgeDocument, KnowledgeChunk, RFPRequest, RFPSection, GeneratedResponse, ComplianceGap


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "doc_type", "uploaded_at"]
    list_filter = ["doc_type"]
    search_fields = ["title"]


@admin.register(RFPRequest)
class RFPRequestAdmin(admin.ModelAdmin):
    list_display = ["title", "issuer", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["title", "issuer"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(GeneratedResponse)
class GeneratedResponseAdmin(admin.ModelAdmin):
    list_display = ["section", "confidence_score", "reviewed", "approved"]
    list_filter = ["reviewed", "approved"]


@admin.register(ComplianceGap)
class ComplianceGapAdmin(admin.ModelAdmin):
    list_display = ["framework", "severity", "response"]
    list_filter = ["framework", "severity"]
