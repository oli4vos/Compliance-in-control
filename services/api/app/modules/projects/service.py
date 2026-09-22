import json

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.modules.projects.models import AuditEvent, Project, ProjectMetrics
from app.modules.projects.schemas import ProjectCreate, ProjectResponse


def _response(project: Project) -> ProjectResponse:
    metrics = project.metrics or ProjectMetrics(project_id=project.id)
    progress = (
        round(metrics.reviewed_count / metrics.requirement_count * 100)
        if metrics.requirement_count
        else 0
    )
    return ProjectResponse(
        id=project.id,
        name=project.name,
        client=project.client,
        reference=project.reference,
        due_date=project.due_date,
        product=project.product,
        product_version=project.product_version,
        owner=project.owner,
        notes=project.notes,
        created_at=project.created_at,
        requirement_count=metrics.requirement_count,
        reviewed_count=metrics.reviewed_count,
        sufficient_count=metrics.sufficient_count,
        missing_count=metrics.missing_count,
        next_deadline=metrics.next_deadline or project.due_date,
        progress=progress,
    )


def list_projects(session: Session) -> list[ProjectResponse]:
    projects = session.scalars(
        select(Project).options(joinedload(Project.metrics)).order_by(Project.created_at.desc())
    ).all()
    return [_response(project) for project in projects]


def get_project(session: Session, project_id: str) -> ProjectResponse | None:
    project = session.scalar(
        select(Project).options(joinedload(Project.metrics)).where(Project.id == project_id)
    )
    return _response(project) if project else None


def create_project(
    session: Session,
    payload: ProjectCreate,
    idempotency_key: str | None = None,
) -> ProjectResponse:
    if idempotency_key:
        existing = session.scalar(
            select(Project)
            .options(joinedload(Project.metrics))
            .where(Project.idempotency_key == idempotency_key)
        )
        if existing:
            return _response(existing)

    project = Project(**payload.model_dump(), idempotency_key=idempotency_key)
    project.metrics = ProjectMetrics()
    session.add(project)
    session.flush()
    session.add(
        AuditEvent(
            project_id=project.id,
            action="Dossier aangemaakt",
            entity=f"Project:{project.id}",
            new_value=json.dumps({"name": project.name, "client": project.client}),
        )
    )
    session.commit()
    session.refresh(project)
    return _response(project)
