from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['organization_id', 'actor_email', 'action', 'object_type', 'timestamp']
    list_filter = ['action', 'object_type']
    search_fields = ['actor_email']
