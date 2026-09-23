import re
from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Header,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database import get_db
from app.modules.projects.documents import discard_upload, save_upload
from app.modules.projects.models import EvidenceDocument
from app.modules.projects.schemas import (
    AssessmentUpsert,
    EvidenceDocumentResponse,
    MutationResult,
    ProjectCreate,
    ProjectResponse,
    RequirementCreate,
    RequirementsMerge,
    RequirementUpdate,
    SourceDocumentResponse,
    WorkspaceResponse,
)
from app.modules.projects.service import create_project, get_project, list_projects
from app.modules.projects.workspace import (
    add_requirement,
    create_evidence_document,
    create_source_document,
    export_csv,
    extract_document_requirements,
    generate_matches,
    get_project_model,
    get_workspace,
    merge_requirements,
    remove_requirement,
    save_assessment,
    update_requirement,
)
from app.seed import seed_demo

router = APIRouter(prefix="/projects", tags=["projects"])
DatabaseSession = Annotated[Session, Depends(get_db)]
DISCLAIMER = (
    "IPC ondersteunt de voorbereiding en beoordeling van bewijsdossiers. "
    "Een voorgestelde koppeling is geen juridisch oordeel, certificering of garantie van naleving."
)


@router.post("/demo/reset", response_model=MutationResult)
def demo_reset(session: DatabaseSession) -> MutationResult:
    if get_settings().environment != "development":
        raise HTTPException(
            status_code=403, detail="Demo-reset is alleen beschikbaar in development."
        )
    seed_demo(session, force=True)
    return MutationResult(count=1)


def _date(value: str) -> date | None:
    return date.fromisoformat(value) if value else None


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


@router.get("/{project_id}/workspace", response_model=WorkspaceResponse)
def project_workspace(project_id: str, session: DatabaseSession) -> WorkspaceResponse:
    return get_workspace(session, project_id)


@router.post(
    "/{project_id}/source-documents",
    response_model=SourceDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def source_document_create(
    project_id: str,
    session: DatabaseSession,
    document_type: Annotated[str, Form(alias="type")],
    file: Annotated[UploadFile, File()],
) -> SourceDocumentResponse:
    settings = get_settings()
    get_project_model(session, project_id)
    upload = await save_upload(project_id, file, settings)
    try:
        document = create_source_document(session, project_id, document_type, upload)
    except Exception:
        session.rollback()
        discard_upload(project_id, upload, settings)
        raise
    return SourceDocumentResponse.model_validate(document)


@router.post(
    "/{project_id}/source-documents/{document_id}/extract",
    response_model=MutationResult,
)
def source_document_extract(
    project_id: str, document_id: str, session: DatabaseSession
) -> MutationResult:
    return extract_document_requirements(session, project_id, document_id)


@router.post("/{project_id}/requirements", response_model=MutationResult)
def requirement_create(
    project_id: str, payload: RequirementCreate, session: DatabaseSession
) -> MutationResult:
    return add_requirement(session, project_id, payload)


@router.patch("/{project_id}/requirements/{requirement_id}", response_model=MutationResult)
def requirement_update(
    project_id: str,
    requirement_id: str,
    payload: RequirementUpdate,
    session: DatabaseSession,
) -> MutationResult:
    return update_requirement(session, project_id, requirement_id, payload)


@router.delete("/{project_id}/requirements/{requirement_id}", response_model=MutationResult)
def requirement_delete(
    project_id: str, requirement_id: str, session: DatabaseSession
) -> MutationResult:
    return remove_requirement(session, project_id, requirement_id)


@router.post("/{project_id}/requirements/merge", response_model=MutationResult)
def requirement_merge(
    project_id: str, payload: RequirementsMerge, session: DatabaseSession
) -> MutationResult:
    return merge_requirements(session, project_id, payload)


@router.post(
    "/{project_id}/evidence-documents",
    response_model=EvidenceDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def evidence_document_create(
    project_id: str,
    session: DatabaseSession,
    file: Annotated[UploadFile, File()],
    title: Annotated[str, Form()] = "",
    document_type: Annotated[str, Form(alias="documentType")] = "overig",
    description: Annotated[str, Form()] = "",
    organization: Annotated[str, Form()] = "",
    product: Annotated[str, Form()] = "",
    product_version: Annotated[str, Form(alias="productVersion")] = "",
    environment: Annotated[str, Form()] = "",
    owner: Annotated[str, Form()] = "",
    issued_at: Annotated[str, Form(alias="issuedAt")] = "",
    expires_at: Annotated[str, Form(alias="expiresAt")] = "",
    confidentiality: Annotated[str, Form()] = "intern",
    tags: Annotated[str, Form()] = "",
) -> EvidenceDocumentResponse:
    settings = get_settings()
    get_project_model(session, project_id)
    upload = await save_upload(project_id, file, settings)
    try:
        document = create_evidence_document(
            session,
            project_id,
            upload,
            title=title,
            document_type=document_type,
            description=description,
            organization=organization,
            product=product,
            product_version=product_version,
            environment=environment,
            owner=owner,
            issued_at=_date(issued_at),
            expires_at=_date(expires_at),
            confidentiality=confidentiality,
            tags=tags,
        )
    except Exception:
        session.rollback()
        discard_upload(project_id, upload, settings)
        raise
    return EvidenceDocumentResponse.model_validate(document)


@router.get("/{project_id}/evidence-documents/{document_id}/file", response_class=FileResponse)
def evidence_document_file(
    project_id: str, document_id: str, session: DatabaseSession
) -> FileResponse:
    document = session.scalar(
        select(EvidenceDocument).where(
            EvidenceDocument.id == document_id, EvidenceDocument.project_id == project_id
        )
    )
    if document is None:
        raise HTTPException(status_code=404, detail="Bestand niet gevonden.")
    if re.sub(r"[^a-zA-Z0-9_-]", "", project_id) != project_id:
        raise HTTPException(status_code=400, detail="Ongeldige bestandsreferentie.")
    upload_root = Path(get_settings().upload_dir).resolve()
    file_path = (upload_root / project_id / document.stored_name).resolve()
    if upload_root not in file_path.parents or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Bestand is niet lokaal aanwezig.")
    download_name = re.sub(r'[\r\n"]', "_", document.file_name)
    return FileResponse(
        file_path,
        media_type=document.mime_type,
        filename=download_name,
        headers={"Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff"},
    )


@router.post("/{project_id}/matches/generate", response_model=MutationResult)
def matches_generate(project_id: str, session: DatabaseSession) -> MutationResult:
    return generate_matches(session, project_id)


@router.put(
    "/{project_id}/requirements/{requirement_id}/assessment",
    response_model=MutationResult,
)
def assessment_save(
    project_id: str,
    requirement_id: str,
    payload: AssessmentUpsert,
    session: DatabaseSession,
) -> MutationResult:
    return save_assessment(session, project_id, requirement_id, payload)


@router.get("/{project_id}/export.csv", response_class=Response)
def project_export(project_id: str, session: DatabaseSession) -> Response:
    contents, filename = export_csv(session, project_id, DISCLAIMER)
    return Response(
        contents,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
