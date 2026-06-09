from django.contrib import admin
from .models import Client, AgencyProject, Asset, AgencyInvoice

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['company_name']

@admin.register(AgencyProject)
class AgencyProjectAdmin(admin.ModelAdmin):
    list_display = ['client', 'name', 'status', 'deadline']
    list_filter = ['status']
    search_fields = ['name']

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['project', 'name', 'asset_type', 'status']
    list_filter = ['status', 'asset_type']
    search_fields = ['name']

@admin.register(AgencyInvoice)
class AgencyInvoiceAdmin(admin.ModelAdmin):
    list_display = ['client', 'total', 'status', 'due_date']
    list_filter = ['status']
