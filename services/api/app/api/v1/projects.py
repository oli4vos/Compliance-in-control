from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.projects.schemas import ProjectCreate, ProjectResponse
from app.modules.projects.service import create_project, get_project, list_projects

router = APIRouter(prefix="/projects", tags=["projects"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[ProjectResponse])
def project_index(session: DatabaseSession) -> list[ProjectResponse]:
    return list_projects(session)


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def project_create(
    payload: ProjectCreate,
    session: DatabaseSession,
    idempotency_key: Annotated[str | None, Header(max_length=100)] = None,
) -> ProjectResponse:
    return create_project(session, payload, idempotency_key)


@router.get("/{project_id}", response_model=ProjectResponse)
def project_detail(project_id: str, session: DatabaseSession) -> ProjectResponse:
    project = get_project(session, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Dossier niet gevonden.")
    return project
