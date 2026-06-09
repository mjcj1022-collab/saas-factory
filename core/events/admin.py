from django.contrib import admin
from .models import DomainEvent

@admin.register(DomainEvent)
class DomainEventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'aggregate_type', 'aggregate_id', 'processed', 'created_at']
    list_filter = ['event_type', 'processed']
