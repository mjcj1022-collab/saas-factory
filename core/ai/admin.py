from django.contrib import admin
from .models import AIRequest

@admin.register(AIRequest)
class AIRequestAdmin(admin.ModelAdmin):
    list_display = ['organization_id', 'provider', 'tokens_used', 'created_at', 'error']
    list_filter = ['provider']
