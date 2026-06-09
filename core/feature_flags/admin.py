from django.contrib import admin
from .models import FeatureFlag

@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ['organization_id', 'key', 'enabled']
    list_filter = ['enabled']
    search_fields = ['key']
