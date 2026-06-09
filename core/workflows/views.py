from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Workflow, WorkflowTrigger, WorkflowAction, WorkflowExecution


class WorkflowTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowTrigger
        fields = ["id", "event_type", "conditions"]


class WorkflowActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowAction
        fields = ["id", "sequence", "action_type", "config", "delay_seconds"]


class WorkflowExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowExecution
        fields = ["id", "status", "context", "started_at", "completed_at", "error"]
        read_only_fields = ["id", "started_at"]


class WorkflowSerializer(serializers.ModelSerializer):
    triggers = WorkflowTriggerSerializer(many=True, read_only=True)
    actions = WorkflowActionSerializer(many=True, read_only=True)

    class Meta:
        model = Workflow
        fields = ["id", "name", "description", "is_active", "created_at", "triggers", "actions"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        validated_data["organization_id"] = self.context["request"].user.organization_id
        return super().create(validated_data)


class WorkflowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkflowSerializer

    def get_queryset(self):
        return Workflow.objects.filter(organization_id=self.request.user.organization_id)

    @action(detail=True, methods=["post"])
    def test_run(self, request, pk=None):
        """Manually trigger a workflow with test payload."""
        workflow = self.get_object()
        from core.events.models import DomainEvent
        from core.workflows.executor import WorkflowExecutor
        import uuid

        # Create a synthetic event
        fake_event = DomainEvent(
            id=uuid.uuid4(),
            organization_id=workflow.organization_id,
            event_type=workflow.triggers.first().event_type if workflow.triggers.exists() else "manual",
            aggregate_type="manual",
            aggregate_id="test",
            payload=request.data.get("payload", {}),
        )
        executions = WorkflowExecutor.run_for_event(fake_event)
        return Response({
            "executions": WorkflowExecutionSerializer(executions, many=True).data
        })

    @action(detail=True, methods=["get"])
    def executions(self, request, pk=None):
        workflow = self.get_object()
        execs = WorkflowExecution.objects.filter(workflow=workflow).order_by("-started_at")[:50]
        return Response(WorkflowExecutionSerializer(execs, many=True).data)
