from celery import shared_task
import logging
logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def analyze_revision_task(self, old_drawing_id: str, new_drawing_id: str):
    """AI-powered drawing revision analysis."""
    try:
        from apps.construction.models import Drawing, RevisionAnalysis, TradePackage, MaterialImpact
        from core.ai.services import AIRouter
        import json

        old = Drawing.objects.get(id=old_drawing_id)
        new = Drawing.objects.get(id=new_drawing_id)

        system = "You are a construction drawing analysis expert. Compare drawing revisions and identify changes."
        prompt = f"""
Compare drawing revision:
OLD: {old.title} Rev {old.revision} ({old.discipline})
NEW: {new.title} Rev {new.revision} ({new.discipline})

Identify changes and affected trades. Return JSON:
{{
  "summary": "brief description",
  "changes": [{{"type": "added|removed|modified", "description": "..."}}],
  "affected_trades": ["electrical", "hvac", ...],
  "material_impacts": [{{"trade": "...", "material": "...", "qty_delta": 0, "unit": "...", "cost_delta": 0}}]
}}
"""
        raw = AIRouter.generate("trade_impact", prompt, system=system, max_tokens=1500)
        raw = raw.strip().removeprefix("```json").removesuffix("```").strip()
        data = json.loads(raw)

        analysis = RevisionAnalysis.objects.create(
            old_drawing=old,
            new_drawing=new,
            differences=data.get("changes", []),
            ai_summary=data.get("summary", ""),
            completed=True,
        )

        for impact in data.get("material_impacts", []):
            trade = TradePackage.objects.filter(
                project=new.project,
                trade_type__icontains=impact.get("trade", ""),
            ).first()
            if trade:
                MaterialImpact.objects.create(
                    revision=analysis,
                    trade=trade,
                    material_name=impact.get("material", ""),
                    quantity_delta=impact.get("qty_delta", 0),
                    unit=impact.get("unit", ""),
                    estimated_cost_delta=impact.get("cost_delta", 0),
                )

        # Notify affected trades
        from core.events.models import EventPublisher
        EventPublisher.publish(
            event_type="drawing.revision_detected",
            aggregate_type="RevisionAnalysis",
            aggregate_id=str(analysis.id),
            payload={"affected_trades": data.get("affected_trades", [])},
            organization_id=new.project.organization_id,
        )

    except Exception as exc:
        logger.exception("analyze_revision_task failed: %s", exc)
        raise self.retry(exc=exc, countdown=30)
