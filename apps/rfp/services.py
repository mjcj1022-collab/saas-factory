"""
RFP Response Matrix — core services.
"""
from __future__ import annotations
import json
from typing import List, Dict


class RFPParser:
    """
    Extracts structured sections from uploaded RFP documents.
    Uses AI to identify question headings and body text.
    """

    def extract_sections(self, document_text: str) -> List[Dict]:
        from core.ai.services import AIRouter

        system = (
            "You are an expert at parsing RFP documents. "
            "Extract all questions and sections as structured JSON."
        )
        prompt = f"""
Parse the following RFP document and extract all sections/questions.
Return ONLY valid JSON array in this format:
[
  {{"heading": "Security", "question": "Describe your MFA implementation.", "category": "security"}},
  ...
]

RFP TEXT:
{document_text[:8000]}
"""
        raw = AIRouter.generate("rfp_response", prompt, system=system, max_tokens=3000)
        raw = raw.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(raw)

    def extract_text_from_pdf(self, file_path: str) -> str:
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)
        except ImportError:
            return ""


class ContextRetriever:
    """
    Semantic search over KnowledgeChunks using pgvector or fallback full-text.
    """

    def __init__(self, organization_id):
        self.organization_id = organization_id

    def search(self, question: str, top_k: int = 5) -> List[Dict]:
        from apps.rfp.models import KnowledgeChunk, KnowledgeDocument
        # Fallback: simple icontains search when embeddings not yet built
        chunks = (
            KnowledgeChunk.objects.filter(
                document__organization_id=self.organization_id,
                chunk_text__icontains=question[:50],
            )
            .select_related("document")[:top_k]
        )
        return [
            {
                "chunk_id": str(c.id),
                "text": c.chunk_text,
                "source": c.document.title,
            }
            for c in chunks
        ]


class ResponseGenerator:
    """
    Generates RFP answers grounded in retrieved context.
    """

    def generate(self, question: str, context_chunks: List[Dict]) -> Dict:
        from core.ai.services import AIRouter

        context_text = "\n\n".join(
            f"[Source: {c['source']}]\n{c['text']}" for c in context_chunks
        )

        system = (
            "You are a technical writer generating RFP responses. "
            "Answer using ONLY the provided context. "
            "If the context does not contain enough information, respond with: NEEDS_HUMAN_REVIEW"
        )
        prompt = f"""
QUESTION:
{question}

CONTEXT:
{context_text}

Write a professional, concise RFP response answer.
"""
        answer = AIRouter.generate("rfp_response", prompt, system=system, max_tokens=1500)
        needs_review = "NEEDS_HUMAN_REVIEW" in answer
        confidence = 0.3 if needs_review else 0.85
        return {"answer": answer, "confidence_score": confidence, "needs_review": needs_review}


class ComplianceEngine:
    """
    Scans generated responses for compliance framework gaps.
    """

    FRAMEWORK_KEYWORDS = {
        "soc2": ["access control", "encryption", "audit", "availability", "confidentiality"],
        "hipaa": ["phi", "protected health", "business associate", "breach notification"],
        "gdpr": ["data subject", "right to erasure", "consent", "dpa", "processor"],
        "iso27001": ["isms", "risk assessment", "asset management", "incident"],
        "fedramp": ["fisma", "nist 800-53", "authorization", "continuous monitoring"],
        "pci_dss": ["cardholder data", "pci", "payment card", "cvv"],
    }

    def scan(self, question: str, answer: str) -> List[Dict]:
        gaps = []
        answer_lower = answer.lower()
        question_lower = question.lower()

        for framework, keywords in self.FRAMEWORK_KEYWORDS.items():
            relevant = any(kw in question_lower for kw in keywords)
            if not relevant:
                continue
            covered = sum(1 for kw in keywords if kw in answer_lower)
            if covered < len(keywords) // 2:
                gaps.append({
                    "framework": framework,
                    "issue": f"Response may not fully address {framework.upper()} requirements.",
                    "recommendation": f"Add specific {framework.upper()} controls and references.",
                    "severity": "high" if covered == 0 else "medium",
                })
        return gaps
