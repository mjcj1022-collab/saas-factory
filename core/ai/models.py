import uuid
from django.db import models


class AIProvider(models.Model):
    PROVIDERS = (
        ("openai", "OpenAI"),
        ("anthropic", "Anthropic"),
        ("gemini", "Google Gemini"),
        ("local", "Local Model"),
    )

    name = models.CharField(max_length=100, choices=PROVIDERS, unique=True)
    api_key_env_var = models.CharField(max_length=100)
    model_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    cost_per_1k_tokens = models.DecimalField(max_digits=8, decimal_places=6, default=0)

    class Meta:
        db_table = "ai_providers"


class AIPromptTemplate(models.Model):
    TASK_TYPES = (
        ("rfp_response", "RFP Response Generation"),
        ("compliance_check", "Compliance Check"),
        ("drawing_analysis", "Drawing Analysis"),
        ("demand_forecast", "Demand Forecast"),
        ("guest_message", "Guest Message"),
        ("trade_impact", "Trade Impact Analysis"),
        ("permit_extract", "Permit Data Extraction"),
        ("maintenance_predict", "Maintenance Prediction"),
        ("route_optimize", "Route Optimization"),
        ("general", "General"),
    )

    name = models.CharField(max_length=255)
    task_type = models.CharField(max_length=100, choices=TASK_TYPES)
    system_prompt = models.TextField()
    user_prompt_template = models.TextField()
    provider = models.ForeignKey(AIProvider, on_delete=models.SET_NULL, null=True)
    max_tokens = models.IntegerField(default=2000)
    temperature = models.FloatField(default=0.3)
    version = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "ai_prompt_templates"


class AIRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    template = models.ForeignKey(AIPromptTemplate, on_delete=models.SET_NULL, null=True)
    provider = models.CharField(max_length=100)
    prompt = models.TextField()
    response = models.TextField(blank=True)
    tokens_used = models.IntegerField(default=0)
    latency_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    error = models.TextField(blank=True)

    class Meta:
        db_table = "ai_requests"


class VectorDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    source_type = models.CharField(max_length=100)
    source_id = models.CharField(max_length=100)
    chunk_text = models.TextField()
    embedding_id = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vector_documents"


class ResponseCache(models.Model):
    prompt_hash = models.CharField(max_length=64, unique=True)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = "response_cache"
