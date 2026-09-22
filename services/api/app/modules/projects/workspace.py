import csv
import io
import json
from datetime import date
from typing import cast

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.core.config import get_settings
from app.modules.projects.adapters import extract_requirement_candidates, propose_evidence
from app.modules.projects.documents import (
    SavedUpload,
    categorize,
    short_title,
)
from app.modules.projects.models import (
    Assessment,
    AuditEvent,
    EvidenceDocument,
    EvidenceMatch,
    Project,
    Requirement,
    SourceDocument,
    Task,
)
from app.modules.projects.schemas import (
    AssessmentUpsert,
    MutationResult,
    RequirementCreate,
    RequirementsMerge,
    RequirementUpdate,
    WorkspaceResponse,
)
from app.modules.projects.service import _response

USER = "Lokale gebruiker"
UNREVIEWED_STATUSES = {"niet beoordeeld", "mogelijk passend"}
MISSING_STATUSES = {"ontbrekend bewijs", "onvoldoende onderbouwd"}


def _project_query(project_id: str):  # type: ignore[no-untyped-def]
    return (
        select(Project)
        .where(Project.id == project_id)
        .options(
            joinedload(Project.metrics),
            selectinload(Project.source_documents),
            selectinload(Project.evidence_documents),
            selectinload(Project.requirements).joinedload(Requirement.source_document),
            selectinload(Project.requirements)
            .selectinload(Requirement.matches)
            .joinedload(EvidenceMatch.evidence_document),
            selectinload(Project.requirements).selectinload(Requirement.assessments),
            selectinload(Project.tasks),
            selectinload(Project.audit_events),
        )
    )


def get_project_model(session: Session, project_id: str) -> Project:
    project = session.scalar(_project_query(project_id).execution_options(populate_existing=True))
    if project is None:
        raise HTTPException(status_code=404, detail="Dossier niet gevonden.")
    return cast(Project, project)


def _audit(
    session: Session,
    project_id: str,
    action: str,
    entity: str,
    old_value: str = "",
    new_value: str = "",
    requirement_id: str | None = None,
    actor: str = USER,
) -> None:
    session.add(
        AuditEvent(
            project_id=project_id,
            requirement_id=requirement_id,
            action=action,
            entity=entity,
            old_value=old_value,
            new_value=new_value,
            actor=actor,
        )
    )


def refresh_metrics(project: Project) -> None:
    requirements = project.requirements
    project.metrics.requirement_count = len(requirements)
    project.metrics.reviewed_count = len(
        [
            requirement
            for requirement in requirements
            if requirement.status not in UNREVIEWED_STATUSES
        ]
    )
    project.metrics.sufficient_count = len(
        [
            requirement
            for requirement in requirements
            if requirement.status == "voldoende onderbouwd"
        ]
    )
    project.metrics.missing_count = len(
        [requirement for requirement in requirements if requirement.status in MISSING_STATUSES]
    )
    deadlines = [task.deadline for task in project.tasks if task.status == "open" and task.deadline]
    project.metrics.next_deadline = min(deadlines) if deadlines else project.due_date


def get_workspace(session: Session, project_id: str) -> WorkspaceResponse:
    project = get_project_model(session, project_id)
    project.source_documents.sort(key=lambda document: document.uploaded_at)
    project.evidence_documents.sort(key=lambda document: document.uploaded_at, reverse=True)
    project.requirements.sort(key=lambda requirement: requirement.number)
    for requirement in project.requirements:
        requirement.matches.sort(key=lambda match: match.score, reverse=True)
        requirement.assessments.sort(key=lambda assessment: assessment.updated_at, reverse=True)
    project.tasks.sort(key=lambda task: task.deadline or date.max)
    project.audit_events.sort(key=lambda event: event.created_at, reverse=True)
    summary = _response(project).model_dump(by_alias=False)
    return WorkspaceResponse.model_validate(
        {
            **summary,
            "source_documents": project.source_documents,
            "evidence_documents": project.evidence_documents,
            "requirements": project.requirements,
            "tasks": project.tasks,
            "audit_events": project.audit_events[:150],
        }
    )


def create_source_document(
    session: Session, project_id: str, document_type: str, upload: SavedUpload
) -> SourceDocument:
    get_project_model(session, project_id)
    document = SourceDocument(
        project_id=project_id,
        name=upload.original_name,
        stored_name=upload.stored_name,
        type=document_type,
        mime_type=upload.mime_type,
        extracted_text=upload.extracted_text,
    )
    session.add(document)
    session.flush()
    _audit(
        session,
        project_id,
        "Brondocument toegevoegd",
        f"SourceDocument:{document.id}",
        new_value=document.name,
    )
    session.commit()
    session.refresh(document)
    return document


def extract_document_requirements(
    session: Session, project_id: str, document_id: str
) -> MutationResult:
    project = get_project_model(session, project_id)
    document = session.scalar(
        select(SourceDocument).where(
            SourceDocument.id == document_id, SourceDocument.project_id == project_id
        )
    )
    if document is None:
        raise HTTPException(status_code=404, detail="Brondocument niet gevonden.")
    candidates, engine = extract_requirement_candidates(document.extracted_text, get_settings())
    existing_numbers = {
        int(requirement.number.split("-")[-1])
        for requirement in project.requirements
        if requirement.number.startswith("E-") and requirement.number.split("-")[-1].isdigit()
    }
    next_number = max(existing_numbers, default=0) + 1
    existing_texts = {requirement.original_text.casefold() for requirement in project.requirements}
    created = 0
    for candidate in candidates:
        if candidate.text.casefold() in existing_texts:
            continue
        requirement = Requirement(
            project_id=project_id,
            source_document_id=document.id,
            number=f"E-{next_number:03d}",
            title=candidate.title,
            original_text=candidate.text,
            category=candidate.category,
            source_location=candidate.location,
            source_fragment=candidate.fragment,
            priority=candidate.priority,
            origin="automatisch",
        )
        session.add(requirement)
        project.requirements.append(requirement)
        existing_texts.add(candidate.text.casefold())
        next_number += 1
        created += 1
    refresh_metrics(project)
    _audit(
        session,
        project_id,
        "Eisen geëxtraheerd",
        f"SourceDocument:{document.id}",
        new_value=f"{created} concept-eisen · {engine}",
    )
    session.commit()
    return MutationResult(count=created)


def add_requirement(
    session: Session, project_id: str, payload: RequirementCreate
) -> MutationResult:
    project = get_project_model(session, project_id)
    numbers = [
        int(requirement.number[2:])
        for requirement in project.requirements
        if requirement.number.startswith("E-") and requirement.number[2:].isdigit()
    ]
    text = payload.original_text.strip()
    requirement = Requirement(
        project_id=project_id,
        number=f"E-{max(numbers, default=0) + 1:03d}",
        title=payload.title.strip() or short_title(text),
        original_text=text,
        category=payload.category or categorize(text),
        source_location="Handmatig toegevoegd",
        source_fragment=text,
        priority=payload.priority,
        origin="handmatig",
    )
    session.add(requirement)
    project.requirements.append(requirement)
    session.flush()
    refresh_metrics(project)
    _audit(
        session,
        project_id,
        "Eis toegevoegd",
        f"Requirement:{requirement.id}",
        new_value=text,
        requirement_id=requirement.id,
    )
    session.commit()
    return MutationResult(count=1)


def update_requirement(
    session: Session, project_id: str, requirement_id: str, payload: RequirementUpdate
) -> MutationResult:
    project = get_project_model(session, project_id)
    requirement = next((item for item in project.requirements if item.id == requirement_id), None)
    if requirement is None:
        raise HTTPException(status_code=404, detail="Eis niet gevonden.")
    old_value = json.dumps({"title": requirement.title, "category": requirement.category})
    requirement.title = payload.title
    requirement.original_text = payload.original_text
    requirement.category = payload.category
    requirement.priority = payload.priority
    requirement.not_applicable = payload.not_applicable
    if payload.not_applicable:
        requirement.status = "niet van toepassing"
    refresh_metrics(project)
    _audit(
        session,
        project_id,
        "Eis bijgewerkt",
        f"Requirement:{requirement.id}",
        old_value=old_value,
        new_value=payload.model_dump_json(),
        requirement_id=requirement.id,
    )
    session.commit()
    return MutationResult(count=1)


def remove_requirement(session: Session, project_id: str, requirement_id: str) -> MutationResult:
    project = get_project_model(session, project_id)
    requirement = next((item for item in project.requirements if item.id == requirement_id), None)
    if requirement is None:
        return MutationResult(count=0)
    old_text = requirement.original_text
    project.requirements.remove(requirement)
    session.delete(requirement)
    session.flush()
    refresh_metrics(project)
    _audit(
        session,
        project_id,
        "Eis verwijderd",
        f"Requirement:{requirement_id}",
        old_value=old_text,
    )
    session.commit()
    return MutationResult(count=1)


def merge_requirements(
    session: Session, project_id: str, payload: RequirementsMerge
) -> MutationResult:
    if payload.primary_id == payload.secondary_id:
        raise HTTPException(status_code=422, detail="Kies twee verschillende eisen.")
    project = get_project_model(session, project_id)
    primary = next((item for item in project.requirements if item.id == payload.primary_id), None)
    secondary = next(
        (item for item in project.requirements if item.id == payload.secondary_id), None
    )
    if primary is None or secondary is None:
        raise HTTPException(status_code=404, detail="Een van de eisen bestaat niet.")
    primary.original_text = (
        f"{primary.original_text}\n\nSamengevoegd met {secondary.number}: {secondary.original_text}"
    )
    primary.source_fragment = f"{primary.source_fragment}\n---\n{secondary.source_fragment}"
    primary.title = f"{primary.title} / {secondary.title}"[:200]
    secondary_number = secondary.number
    project.requirements.remove(secondary)
    session.delete(secondary)
    session.flush()
    refresh_metrics(project)
    _audit(
        session,
        project_id,
        "Eisen samengevoegd",
        f"Requirement:{primary.id}",
        old_value=secondary_number,
        new_value=primary.number,
        requirement_id=primary.id,
    )
    session.commit()
    return MutationResult(count=1)


def create_evidence_document(
    session: Session,
    project_id: str,
    upload: SavedUpload,
    *,
    title: str,
    document_type: str,
    description: str,
    organization: str,
    product: str,
    product_version: str,
    environment: str,
    owner: str,
    issued_at: date | None,
    expires_at: date | None,
    confidentiality: str,
    tags: str,
) -> EvidenceDocument:
    get_project_model(session, project_id)
    document = EvidenceDocument(
        project_id=project_id,
        title=title or upload.original_name,
        document_type=document_type,
        description=description,
        organization=organization,
        product=product,
        product_version=product_version,
        environment=environment,
        owner=owner,
        issued_at=issued_at,
        expires_at=expires_at,
        confidentiality=confidentiality,
        tags=tags,
        file_name=upload.original_name,
        stored_name=upload.stored_name,
        mime_type=upload.mime_type,
        extracted_text=upload.extracted_text,
    )
    session.add(document)
    session.flush()
    _audit(
        session,
        project_id,
        "Bewijsstuk toegevoegd",
        f"EvidenceDocument:{document.id}",
        new_value=document.title,
    )
    session.commit()
    session.refresh(document)
    return document


def generate_matches(session: Session, project_id: str) -> MutationResult:
    project = get_project_model(session, project_id)
    count = 0
    engines: set[str] = set()
    for requirement in project.requirements:
        proposals, engine = propose_evidence(
            requirement, project.evidence_documents, project, get_settings()
        )
        engines.add(engine)
        proposal_ids = {proposal.evidence_document_id for proposal in proposals}
        session.execute(
            delete(EvidenceMatch).where(
                EvidenceMatch.requirement_id == requirement.id,
                EvidenceMatch.evidence_document_id.not_in(proposal_ids),
            )
        )
        existing = {match.evidence_document_id: match for match in requirement.matches}
        for proposal in proposals:
            match = existing.get(proposal.evidence_document_id)
            if match is None:
                match = EvidenceMatch(
                    requirement_id=requirement.id,
                    evidence_document_id=proposal.evidence_document_id,
                    score=proposal.score,
                    fragment=proposal.fragment,
                    source_location=proposal.source_location,
                    explanation=proposal.explanation,
                    warnings=proposal.warnings,
                )
                session.add(match)
            else:
                match.score = proposal.score
                match.fragment = proposal.fragment
                match.source_location = proposal.source_location
                match.explanation = proposal.explanation
                match.warnings = proposal.warnings
            count += 1
    _audit(
        session,
        project_id,
        "Bewijsvoorstellen gegenereerd",
        "Project",
        new_value=", ".join(sorted(engines)) or "Geen voorstellen",
    )
    session.commit()
    return MutationResult(count=count)


def save_assessment(
    session: Session,
    project_id: str,
    requirement_id: str,
    payload: AssessmentUpsert,
) -> MutationResult:
    project = get_project_model(session, project_id)
    requirement = next((item for item in project.requirements if item.id == requirement_id), None)
    if requirement is None:
        raise HTTPException(status_code=404, detail="Eis niet gevonden.")
    if payload.evidence_match_id and not any(
        match.id == payload.evidence_match_id for match in requirement.matches
    ):
        raise HTTPException(
            status_code=422, detail="Het gekozen bewijsvoorstel hoort niet bij deze eis."
        )
    assessment = requirement.assessments[0] if requirement.assessments else None
    if assessment is None:
        assessment = Assessment(requirement_id=requirement.id, status=payload.status)
        session.add(assessment)
        requirement.assessments.append(assessment)
    old_status = requirement.status
    assessment.evidence_match_id = payload.evidence_match_id
    assessment.status = payload.status
    assessment.draft_answer = payload.draft_answer
    assessment.notes = payload.notes
    assessment.owner = payload.owner
    assessment.deadline = payload.deadline
    assessment.approved = payload.approved
    assessment.assessed_by = USER
    requirement.status = payload.status

    task = next((item for item in project.tasks if item.requirement_id == requirement.id), None)
    if payload.deadline:
        if task is None:
            task = Task(
                project_id=project_id,
                requirement_id=requirement.id,
                title=f"Beoordeling afronden voor {requirement.number}",
                owner=payload.owner,
                deadline=payload.deadline,
            )
            session.add(task)
            project.tasks.append(task)
        else:
            task.owner = payload.owner
            task.deadline = payload.deadline
        task.status = "afgerond" if payload.status == "voldoende onderbouwd" else "open"
    elif task is not None:
        session.delete(task)
        project.tasks.remove(task)
    refresh_metrics(project)
    _audit(
        session,
        project_id,
        "Menselijke beoordeling vastgelegd",
        f"Requirement:{requirement.id}",
        old_value=old_status,
        new_value=payload.status,
        requirement_id=requirement.id,
    )
    session.commit()
    return MutationResult(count=1)


def export_csv(session: Session, project_id: str, disclaimer: str) -> tuple[str, str]:
    workspace = get_workspace(session, project_id)
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter=";", quoting=csv.QUOTE_ALL)
    writer.writerow(["DISCLAIMER", disclaimer])
    writer.writerow([])
    writer.writerow(
        [
            "Nummer",
            "Titel",
            "Categorie",
            "Verplicht/wens",
            "Bronbestand",
            "Bronlocatie",
            "Oorspronkelijke eis",
            "Bronfragment",
            "Menselijke status",
            "Gekoppeld bewijs",
            "Bewijsfragment",
            "Matchscore",
            "Waarschuwingen",
            "Conceptantwoord",
            "Opmerkingen",
            "Eigenaar",
            "Beoordelingsdatum",
        ]
    )
    for requirement in workspace.requirements:
        assessment = requirement.assessments[0] if requirement.assessments else None
        selected = None
        if assessment and assessment.evidence_match_id:
            selected = next(
                (
                    match
                    for match in requirement.matches
                    if match.id == assessment.evidence_match_id
                ),
                None,
            )
        selected = selected or (requirement.matches[0] if requirement.matches else None)
        writer.writerow(
            [
                requirement.number,
                requirement.title,
                requirement.category,
                requirement.priority,
                requirement.source_document.name if requirement.source_document else "Handmatig",
                requirement.source_location,
                requirement.original_text,
                requirement.source_fragment,
                requirement.status,
                selected.evidence_document.title if selected else "",
                selected.fragment if selected else "",
                selected.score if selected else "",
                selected.warnings if selected else "",
                assessment.draft_answer if assessment else "",
                assessment.notes if assessment else "",
                assessment.owner if assessment else "",
                assessment.assessed_at.isoformat() if assessment else "",
            ]
        )
    filename = f"{workspace.reference or 'dossier'}-eisen-bewijsmatrix.csv"
    return "\ufeff" + output.getvalue(), filename
