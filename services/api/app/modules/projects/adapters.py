import json

import httpx

from app.core.config import Settings
from app.modules.projects.documents import RequirementCandidate, extract_requirements
from app.modules.projects.matching import MatchProposal, match_evidence
from app.modules.projects.models import EvidenceDocument, Project, Requirement


def extract_requirement_candidates(
    text: str, settings: Settings
) -> tuple[list[RequirementCandidate], str]:
    if not settings.openai_api_key:
        return extract_requirements(text), "lokale heuristiek"
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "requirements": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        key: {"type": "string"}
                        for key in (
                            "text",
                            "title",
                            "category",
                            "location",
                            "fragment",
                            "priority",
                        )
                    },
                    "required": [
                        "text",
                        "title",
                        "category",
                        "location",
                        "fragment",
                        "priority",
                    ],
                },
            }
        },
        "required": ["requirements"],
    }
    try:
        response = _responses_call(
            settings,
            instructions=(
                "Extraheer uitsluitend expliciete Nederlandse eisen. Bewaar de letterlijke "
                "eistekst, het bronfragment en de locatie. Geef geen juridisch oordeel."
            ),
            input_text=text[:45_000],
            schema_name="requirements",
            schema=schema,
        )
        items = json.loads(response).get("requirements", [])
        candidates = [
            RequirementCandidate(
                text=item["text"],
                title=item["title"][:200],
                category=item["category"][:80],
                location=item["location"][:160],
                fragment=item["fragment"] if item["fragment"] in text else item["text"],
                priority="wens" if item["priority"] == "wens" else "verplicht",
            )
            for item in items[:80]
            if item.get("text")
        ]
        return candidates, "OpenAI Responses API"
    except (httpx.HTTPError, KeyError, StopIteration, TypeError, ValueError):
        return extract_requirements(text), "lokale heuristiek (AI-fallback)"


def propose_evidence(
    requirement: Requirement,
    evidence: list[EvidenceDocument],
    project: Project,
    settings: Settings,
) -> tuple[list[MatchProposal], str]:
    if not settings.openai_api_key:
        return match_evidence(requirement, evidence, project), "lokale matcher"
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "matches": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "evidenceDocumentId": {"type": "string"},
                        "fragment": {"type": "string"},
                        "sourceLocation": {"type": "string"},
                        "score": {"type": "integer", "minimum": 0, "maximum": 100},
                        "explanation": {"type": "string"},
                        "warnings": {"type": "string"},
                    },
                    "required": [
                        "evidenceDocumentId",
                        "fragment",
                        "sourceLocation",
                        "score",
                        "explanation",
                        "warnings",
                    ],
                },
            }
        },
        "required": ["matches"],
    }
    input_data = {
        "requirement": {
            "text": requirement.original_text,
            "category": requirement.category,
        },
        "project": {"product": project.product, "version": project.product_version},
        "evidence": [
            {
                "id": document.id,
                "title": document.title,
                "organization": document.organization,
                "product": document.product,
                "version": document.product_version,
                "environment": document.environment,
                "expiresAt": document.expires_at.isoformat() if document.expires_at else None,
                "text": document.extracted_text[:9_000],
            }
            for document in evidence
        ],
    }
    try:
        response = _responses_call(
            settings,
            instructions=(
                "Stel mogelijke bewijsrelaties voor, nooit een definitief complianceoordeel. "
                "Het fragment moet letterlijk uit het bewijs komen. Benoem scope-, versie-, "
                "entiteits-, omgevings- en geldigheidsrisico's."
            ),
            input_text=json.dumps(input_data, ensure_ascii=False),
            schema_name="matches",
            schema=schema,
        )
        documents = {document.id: document for document in evidence}
        proposals = []
        for item in json.loads(response).get("matches", []):
            document = documents.get(item["evidenceDocumentId"])
            if document is None:
                continue
            literal = item["fragment"] in document.extracted_text
            warnings = item["warnings"]
            if not literal:
                warnings = (
                    f"{warnings} Geen verifieerbaar letterlijk fragment; zwak voorstel.".strip()
                )
            proposals.append(
                MatchProposal(
                    evidence_document_id=document.id,
                    fragment=item["fragment"] if literal else "",
                    source_location=item["sourceLocation"][:160],
                    score=max(0, min(100, int(item["score"]))),
                    explanation=item["explanation"],
                    warnings=warnings,
                )
            )
        return proposals[:5], "OpenAI Responses API"
    except (httpx.HTTPError, KeyError, StopIteration, TypeError, ValueError):
        return match_evidence(requirement, evidence, project), "lokale matcher (AI-fallback)"


def _responses_call(
    settings: Settings,
    *,
    instructions: str,
    input_text: str,
    schema_name: str,
    schema: dict[str, object],
) -> str:
    response = httpx.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {settings.openai_api_key}"},
        json={
            "model": settings.openai_model,
            "store": False,
            "instructions": instructions,
            "input": input_text,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "strict": True,
                    "schema": schema,
                }
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    output_text = next(
        content["text"]
        for output in payload.get("output", [])
        for content in output.get("content", [])
        if content.get("type") == "output_text"
    )
    if not isinstance(output_text, str):
        raise TypeError("De AI-response bevat geen tekst.")
    return output_text
