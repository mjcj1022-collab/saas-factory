from django.contrib import admin
from .models import Integration

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'category', 'enabled']
    list_filter = ['category', 'enabled']
    search_fields = ['name', 'provider']
