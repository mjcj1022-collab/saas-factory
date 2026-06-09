from rest_framework import serializers
from .models import (
    FranchiseBrand, Franchisee, FranchiseLocation,
    Milestone, ComplianceScore, TrainingModule, TrainingCompletion, ConstructionPhase,
)


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ["id", "title", "description", "due_date", "completed", "completed_at", "sequence"]
        read_only_fields = ["id", "completed_at"]


class ComplianceScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceScore
        fields = ["score", "risk_level", "findings", "last_assessed"]
        read_only_fields = ["last_assessed"]


class ConstructionPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionPhase
        fields = ["id", "phase_name", "percent_complete", "start_date", "end_date", "notes"]
        read_only_fields = ["id"]


class FranchiseLocationSerializer(serializers.ModelSerializer):
    milestones = MilestoneSerializer(many=True, read_only=True)
    compliance_score = ComplianceScoreSerializer(read_only=True)
    construction_phases = ConstructionPhaseSerializer(many=True, read_only=True)
    days_to_open = serializers.SerializerMethodField()

    class Meta:
        model = FranchiseLocation
        fields = [
            "id", "address", "latitude", "longitude", "launch_status",
            "opening_date", "target_open_date", "created_at",
            "days_to_open", "milestones", "compliance_score", "construction_phases",
        ]
        read_only_fields = ["id", "created_at"]

    def get_days_to_open(self, obj):
        if obj.target_open_date:
            from django.utils import timezone
            delta = obj.target_open_date - timezone.now().date()
            return delta.days
        return None


class FranchiseeSerializer(serializers.ModelSerializer):
    locations = FranchiseLocationSerializer(many=True, read_only=True)
    location_count = serializers.SerializerMethodField()

    class Meta:
        model = Franchisee
        fields = [
            "id", "full_name", "email", "phone", "status",
            "net_worth", "liquid_capital", "created_at",
            "location_count", "locations",
        ]
        read_only_fields = ["id", "created_at"]

    def get_location_count(self, obj):
        return obj.locations.count()


class FranchiseBrandSerializer(serializers.ModelSerializer):
    franchisee_count = serializers.SerializerMethodField()
    open_locations = serializers.SerializerMethodField()

    class Meta:
        model = FranchiseBrand
        fields = ["id", "name", "industry", "logo_url", "royalty_rate", "created_at", "franchisee_count", "open_locations"]
        read_only_fields = ["id", "created_at"]

    def get_franchisee_count(self, obj):
        return obj.franchisees.count()

    def get_open_locations(self, obj):
        return FranchiseLocation.objects.filter(franchisee__brand=obj, launch_status="open").count()

    def create(self, validated_data):
        validated_data["organization_id"] = self.context["request"].user.organization_id
        return super().create(validated_data)


class TrainingModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingModule
        fields = ["id", "title", "description", "content_type", "content_url", "duration_minutes", "is_required", "sequence"]
        read_only_fields = ["id"]
