from rest_framework import serializers
from .models import Project, Drawing, RevisionAnalysis, TradePackage, MaterialImpact, DailyReport, PunchItem


class TradePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradePackage
        fields = ["id", "trade_type", "company_name", "contact_email", "contact_phone"]
        read_only_fields = ["id"]


class MaterialImpactSerializer(serializers.ModelSerializer):
    trade_name = serializers.CharField(source="trade.company_name", read_only=True)

    class Meta:
        model = MaterialImpact
        fields = ["id", "trade", "trade_name", "material_name", "quantity_delta", "unit", "estimated_cost_delta", "notes"]


class RevisionAnalysisSerializer(serializers.ModelSerializer):
    material_impacts = MaterialImpactSerializer(many=True, read_only=True)

    class Meta:
        model = RevisionAnalysis
        fields = ["id", "old_drawing", "new_drawing", "differences", "ai_summary", "completed", "analyzed_at", "material_impacts"]
        read_only_fields = ["id", "analyzed_at"]


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ["id", "project", "drawing_number", "title", "discipline", "file", "revision", "revision_date", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class PunchItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PunchItem
        fields = ["id", "title", "description", "status", "assigned_trade", "due_date", "photos", "created_at"]
        read_only_fields = ["id", "created_at"]


class DailyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReport
        fields = ["id", "report_date", "weather", "crew_count", "progress_notes", "issues", "photos", "created_at"]
        read_only_fields = ["id", "created_at"]


class ProjectSerializer(serializers.ModelSerializer):
    drawing_count = serializers.SerializerMethodField()
    open_punch_items = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "name", "address", "project_number", "status", "start_date", "completion_date", "budget", "created_at", "drawing_count", "open_punch_items"]
        read_only_fields = ["id", "created_at"]

    def get_drawing_count(self, obj):
        return obj.drawings.count()

    def get_open_punch_items(self, obj):
        return obj.punch_items.filter(status__in=["open", "in_progress"]).count()

    def create(self, validated_data):
        validated_data["organization_id"] = self.context["request"].user.organization_id
        return super().create(validated_data)
