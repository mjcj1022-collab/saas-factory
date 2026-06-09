"""
Workflow Engine — executes configured workflows in response to domain events.

Usage:
    WorkflowExecutor.run_for_event(event)

To register a workflow in the DB:
    1. Create a Workflow with name
    2. Add WorkflowTrigger with event_type = "rfp.uploaded"
    3. Add WorkflowAction(s) with action_type + config

The executor loops through matching triggers → runs actions sequentially.
"""
from __future__ import annotations
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class WorkflowExecutor:

    @classmethod
    def run_for_event(cls, event) -> list:
        """Find all active workflows triggered by this event and execute them."""
        from core.workflows.models import Workflow, WorkflowTrigger, WorkflowExecution
        from django.utils import timezone

        triggers = WorkflowTrigger.objects.filter(
            event_type=event.event_type,
            workflow__is_active=True,
            workflow__organization_id=event.organization_id,
        ).select_related("workflow")

        executions = []
        for trigger in triggers:
            execution = WorkflowExecution.objects.create(
                workflow=trigger.workflow,
                trigger_event_id=event.id,
                status="running",
                context=event.payload,
            )
            try:
                cls._execute(trigger.workflow, execution, event.payload)
                execution.status = "completed"
                execution.completed_at = timezone.now()
            except Exception as exc:
                execution.status = "failed"
                execution.error = str(exc)
                logger.exception("Workflow %s failed: %s", trigger.workflow.name, exc)
            execution.save()
            executions.append(execution)
        return executions

    @classmethod
    def _execute(cls, workflow, execution, context: Dict[str, Any]):
        from core.workflows.models import WorkflowAction

        actions = WorkflowAction.objects.filter(
            workflow=workflow
        ).order_by("sequence")

        for action in actions:
            cls._run_action(action, context, execution)

    @classmethod
    def _run_action(cls, action, context: Dict[str, Any], execution):
        handler = ACTION_HANDLERS.get(action.action_type)
        if handler:
            handler(action.config, context, execution)
        else:
            logger.warning("Unknown action type: %s", action.action_type)


# ─── Action Handlers ──────────────────────────────────────────────────────────

def _send_notification(config: dict, context: dict, execution):
    from core.notifications.models import Notification
    Notification.objects.create(
        organization_id=execution.workflow.organization_id,
        channel=config.get("channel", "email"),
        recipient=config.get("recipient", ""),
        subject=config.get("subject", "Workflow Notification"),
        message=config.get("message", "").format(**context),
    )


def _create_task(config: dict, context: dict, execution):
    """Generic task creation — extend per vertical."""
    logger.info("create_task action: %s ctx=%s", config, context)


def _call_webhook(config: dict, context: dict, execution):
    import requests
    url = config.get("url")
    if url:
        try:
            requests.post(url, json={"context": context, "workflow": str(execution.workflow_id)}, timeout=10)
        except requests.RequestException as exc:
            logger.warning("Webhook call failed: %s", exc)


def _update_record(config: dict, context: dict, execution):
    """
    config: {model: "apps.rfp.models.RFPRequest", id_field: "rfp_id", updates: {...}}
    """
    from django.apps import apps
    model_path = config.get("model", "")
    try:
        app_label, model_name = model_path.rsplit(".", 1)
        # Simplified: use context to get record id
        record_id = context.get(config.get("id_field", "id"))
        if record_id:
            Model = apps.get_model(app_label, model_name)
            Model.objects.filter(id=record_id).update(**config.get("updates", {}))
    except Exception as exc:
        logger.warning("update_record failed: %s", exc)


def _ai_generate(config: dict, context: dict, execution):
    from core.ai.services import AIRouter
    task_type = config.get("task_type", "general")
    prompt = config.get("prompt_template", "").format(**context)
    result = AIRouter.generate(task_type, prompt, organization_id=execution.workflow.organization_id)
    # Store result back into execution context
    execution.context[config.get("output_key", "ai_result")] = result
    execution.save(update_fields=["context"])


ACTION_HANDLERS = {
    "send_notification": _send_notification,
    "create_task": _create_task,
    "call_webhook": _call_webhook,
    "update_record": _update_record,
    "ai_generate": _ai_generate,
}
