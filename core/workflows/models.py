import uuid
from django.db import models


class Workflow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "workflows"


class WorkflowTrigger(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="triggers")
    event_type = models.CharField(max_length=255)
    conditions = models.JSONField(default=dict)

    class Meta:
        db_table = "workflow_triggers"


class WorkflowAction(models.Model):
    ACTION_TYPES = (
        ("send_notification", "Send Notification"),
        ("create_task", "Create Task"),
        ("create_work_order", "Create Work Order"),
        ("generate_document", "Generate Document"),
        ("call_webhook", "Call Webhook"),
        ("update_record", "Update Record"),
        ("ai_generate", "AI Generate"),
        ("send_email", "Send Email"),
        ("send_sms", "Send SMS"),
    )

    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="actions")
    sequence = models.IntegerField(default=0)
    action_type = models.CharField(max_length=100, choices=ACTION_TYPES)
    config = models.JSONField(default=dict)
    delay_seconds = models.IntegerField(default=0)

    class Meta:
        db_table = "workflow_actions"
        ordering = ["sequence"]


class WorkflowExecution(models.Model):
    STATUS = (
        ("pending", "Pending"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    trigger_event_id = models.UUIDField(null=True)
    status = models.CharField(max_length=50, choices=STATUS, default="pending")
    context = models.JSONField(default=dict)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
    error = models.TextField(blank=True)

    class Meta:
        db_table = "workflow_executions"
