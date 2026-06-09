import uuid
from django.db import models


class KnowledgeDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="knowledge/", blank=True)
    content = models.TextField(blank=True)
    doc_type = models.CharField(max_length=100, default="policy")
    tags = models.JSONField(default=list)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rfp_knowledge_documents"


class KnowledgeChunk(models.Model):
    document = models.ForeignKey(KnowledgeDocument, on_delete=models.CASCADE, related_name="chunks")
    chunk_text = models.TextField()
    embedding_id = models.CharField(max_length=255, blank=True)
    sequence = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict)

    class Meta:
        db_table = "rfp_knowledge_chunks"


class RFPRequest(models.Model):
    STATUS = (
        ("uploaded", "Uploaded"),
        ("parsing", "Parsing"),
        ("generating", "Generating"),
        ("review", "Review"),
        ("approved", "Approved"),
        ("exported", "Exported"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    title = models.CharField(max_length=255)
    original_file = models.FileField(upload_to="rfps/")
    issuer = models.CharField(max_length=255, blank=True)
    due_date = models.DateField(null=True)
    status = models.CharField(max_length=50, choices=STATUS, default="uploaded")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rfp_requests"


class RFPSection(models.Model):
    rfp = models.ForeignKey(RFPRequest, on_delete=models.CASCADE, related_name="sections")
    heading = models.CharField(max_length=255)
    question = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    sequence = models.IntegerField(default=0)
    is_required = models.BooleanField(default=True)

    class Meta:
        db_table = "rfp_sections"
        ordering = ["sequence"]


class GeneratedResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.OneToOneField(RFPSection, on_delete=models.CASCADE, related_name="response")
    answer = models.TextField()
    confidence_score = models.FloatField(default=0.0)
    source_chunks = models.JSONField(default=list)
    reviewed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    reviewer_notes = models.TextField(blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rfp_generated_responses"


class ComplianceGap(models.Model):
    SEVERITIES = (
        ("critical", "Critical"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    )
    FRAMEWORKS = (
        ("soc2", "SOC 2"),
        ("iso27001", "ISO 27001"),
        ("hipaa", "HIPAA"),
        ("gdpr", "GDPR"),
        ("fedramp", "FedRAMP"),
        ("pci_dss", "PCI-DSS"),
    )

    response = models.ForeignKey(GeneratedResponse, on_delete=models.CASCADE, related_name="compliance_gaps")
    framework = models.CharField(max_length=50, choices=FRAMEWORKS)
    issue = models.TextField()
    recommendation = models.TextField(blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITIES)

    class Meta:
        db_table = "rfp_compliance_gaps"
