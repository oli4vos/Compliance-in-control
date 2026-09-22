import re
import unicodedata
from dataclasses import dataclass
from datetime import date

from app.modules.projects.models import EvidenceDocument, Project, Requirement

STOP_WORDS = {
    "de",
    "het",
    "een",
    "en",
    "van",
    "voor",
    "dat",
    "met",
    "moet",
    "dient",
    "worden",
    "zijn",
    "aan",
    "op",
    "in",
    "te",
}


@dataclass(frozen=True)
class MatchProposal:
    evidence_document_id: str
    fragment: str
    source_location: str
    score: int
    explanation: str
    warnings: str


def tokens(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFD", text.lower())
    plain = "".join(character for character in normalized if not unicodedata.combining(character))
    return list(
        dict.fromkeys(
            token for token in re.findall(r"[a-z0-9-]{3,}", plain) if token not in STOP_WORDS
        )
    )


def _category_terms(category: str) -> list[str]:
    descriptions = {
        "informatiebeveiliging": "beveiliging encryptie logging toegang audit",
        "privacy": "privacy persoonsgegevens bewaartermijn subverwerker eer",
        "AI en algoritmen": "algoritme model ai menselijk uitleg",
        "continuïteit": "continuïteit herstel beschikbaarheid",
    }
    return tokens(descriptions.get(category, category))


def _overlap(text: str, requirement_tokens: list[str]) -> int:
    available = set(tokens(text))
    return len([token for token in requirement_tokens if token in available])


def match_evidence(
    requirement: Requirement, evidence: list[EvidenceDocument], project: Project
) -> list[MatchProposal]:
    requirement_tokens = tokens(
        f"{requirement.title} {requirement.original_text} {requirement.category}"
    )
    proposals: list[MatchProposal] = []
    for document in evidence:
        document_tokens = set(
            tokens(
                f"{document.title} {document.description} {document.tags} {document.extracted_text}"
            )
        )
        shared = [token for token in requirement_tokens if token in document_tokens]
        boost = (
            18
            if any(term in document_tokens for term in _category_terms(requirement.category))
            else 0
        )
        score = min(96, round(len(shared) / max(len(requirement_tokens), 1) * 100 + boost))
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+|\n+", document.extracted_text)
            if sentence.strip()
        ]
        fragment = max(
            sentences,
            key=lambda sentence: _overlap(sentence, requirement_tokens),
            default="",
        )[:700]
        warnings: list[str] = []
        if document.product and document.product.casefold() not in {
            project.product.casefold(),
            "organisatiebreed",
        }:
            warnings.append(f"Productscope wijkt af ({document.product}).")
        if document.product_version and document.product_version != project.product_version:
            warnings.append(
                f"Versie {document.product_version} wijkt af van {project.product_version}."
            )
        if document.expires_at and document.expires_at < date.today():
            warnings.append("Bewijsstuk is verlopen.")
        if not fragment:
            warnings.append("Geen letterlijk bronfragment gevonden; zwak voorstel.")
        if score >= 10:
            proposals.append(
                MatchProposal(
                    evidence_document_id=document.id,
                    fragment=fragment,
                    source_location="Geëxtraheerde tekst",
                    score=score,
                    explanation=(
                        f"Overlap op: {', '.join(shared[:5])}."
                        if shared
                        else "Beperkte inhoudelijke overlap; handmatige controle nodig."
                    ),
                    warnings=" ".join(warnings),
                )
            )
    return sorted(proposals, key=lambda proposal: proposal.score, reverse=True)[:5]
