from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def parse_rfp_task(self, rfp_id: str):
    """Extract sections from uploaded RFP document."""
    try:
        from apps.rfp.models import RFPRequest, RFPSection
        from apps.rfp.services import RFPParser

        rfp = RFPRequest.objects.get(id=rfp_id)
        rfp.status = "parsing"
        rfp.save(update_fields=["status"])

        parser = RFPParser()
        text = parser.extract_text_from_pdf(rfp.original_file.path)
        sections = parser.extract_sections(text)

        for i, sec in enumerate(sections):
            RFPSection.objects.create(
                rfp=rfp,
                heading=sec.get("heading", ""),
                question=sec.get("question", ""),
                category=sec.get("category", ""),
                sequence=i,
            )

        rfp.status = "generating"
        rfp.save(update_fields=["status"])
        generate_responses_task.delay(rfp_id)
    except Exception as exc:
        logger.exception("parse_rfp_task failed: %s", exc)
        raise self.retry(exc=exc, countdown=30)


@shared_task(bind=True, max_retries=3)
def generate_responses_task(self, rfp_id: str):
    """Generate AI responses for all RFP sections."""
    try:
        from apps.rfp.models import RFPRequest, RFPSection, GeneratedResponse
        from apps.rfp.services import ContextRetriever, ResponseGenerator, ComplianceEngine

        rfp = RFPRequest.objects.get(id=rfp_id)
        retriever = ContextRetriever(rfp.organization_id)
        generator = ResponseGenerator()
        compliance = ComplianceEngine()

        for section in rfp.sections.all():
            chunks = retriever.search(section.question)
            result = generator.generate(section.question, chunks)
            response = GeneratedResponse.objects.create(
                section=section,
                answer=result["answer"],
                confidence_score=result["confidence_score"],
                source_chunks=chunks,
            )
            gaps = compliance.scan(section.question, result["answer"])
            from apps.rfp.models import ComplianceGap
            for gap in gaps:
                ComplianceGap.objects.create(response=response, **gap)

        rfp.status = "review"
        rfp.save(update_fields=["status"])
    except Exception as exc:
        logger.exception("generate_responses_task failed: %s", exc)
        raise self.retry(exc=exc, countdown=60)


@shared_task
def export_rfp_task(rfp_id: str, format: str = "docx"):
    """Export approved RFP responses to DOCX or PDF."""
    from apps.rfp.models import RFPRequest
    rfp = RFPRequest.objects.get(id=rfp_id)
    # Document generation plugs into platform.documents engine
    logger.info("Exporting RFP %s as %s", rfp_id, format)
