from rest_framework import serializers
from .models import Client, AgencyProject, Asset, AssetVersion, ApprovalRequest, AgencyInvoice

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'company_name', 'contact_name', 'contact_email', 'monthly_retainer', 'is_active']
        read_only_fields = ['id']

class AgencyProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyProject
        fields = ['id', 'client', 'name', 'status', 'start_date', 'deadline', 'budget']
        read_only_fields = ['id']

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'project', 'name', 'asset_type', 'status', 'file_url', 'created_at']
        read_only_fields = ['id']

class AssetVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetVersion
        fields = ['id', 'asset', 'version_number', 'file_url', 'notes', 'created_at']
        read_only_fields = ['id']

class ApprovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = ['id', 'asset', 'version', 'status', 'client_notes', 'sent_at', 'responded_at']
        read_only_fields = ['id']

class AgencyInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyInvoice
        fields = ['id', 'client', 'project', 'total', 'status', 'due_date', 'paid_at']
        read_only_fields = ['id']
