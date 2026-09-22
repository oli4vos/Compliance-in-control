from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


def to_camel(value: str) -> str:
    first, *rest = value.split("_")
    return first + "".join(word.capitalize() for word in rest)


class ApiModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )


class ProjectCreate(ApiModel):
    name: str = Field(min_length=1, max_length=200)
    client: str = Field(min_length=1, max_length=200)
    reference: str = Field(default="", max_length=100)
    due_date: date | None = None
    product: str = Field(default="", max_length=200)
    product_version: str = Field(default="", max_length=100)
    owner: str = Field(default="", max_length=200)
    notes: str = Field(default="", max_length=5000)


class ProjectResponse(ApiModel):
    id: str
    name: str
    client: str
    reference: str
    due_date: date | None
    product: str
    product_version: str
    owner: str
    notes: str
    created_at: datetime
    requirement_count: int = 0
    reviewed_count: int = 0
    sufficient_count: int = 0
    missing_count: int = 0
    next_deadline: date | None = None
    progress: int = 0


class SourceDocumentResponse(ApiModel):
    id: str
    project_id: str
    name: str
    stored_name: str
    type: str
    mime_type: str
    extracted_text: str
    uploaded_at: datetime


class EvidenceDocumentResponse(ApiModel):
    id: str
    project_id: str
    title: str
    document_type: str
    description: str
    organization: str
    product: str
    product_version: str
    environment: str
    owner: str
    issued_at: date | None
    expires_at: date | None
    confidentiality: str
    tags: str
    file_name: str
    stored_name: str
    mime_type: str
    extracted_text: str
    uploaded_at: datetime


class EvidenceMatchResponse(ApiModel):
    id: str
    requirement_id: str
    evidence_document_id: str
    fragment: str
    source_location: str
    score: int
    explanation: str
    warnings: str
    proposal_status: str
    created_at: datetime
    evidence_document: EvidenceDocumentResponse


class AssessmentResponse(ApiModel):
    id: str
    requirement_id: str
    evidence_match_id: str | None
    status: str
    draft_answer: str
    notes: str
    owner: str
    deadline: date | None
    approved: bool
    assessed_by: str
    assessed_at: datetime
    updated_at: datetime


class RequirementResponse(ApiModel):
    id: str
    project_id: str
    source_document_id: str | None
    number: str
    title: str
    original_text: str
    category: str
    source_location: str
    source_fragment: str
    priority: str
    origin: str
    status: str
    not_applicable: bool
    created_at: datetime
    source_document: SourceDocumentResponse | None
    matches: list[EvidenceMatchResponse]
    assessments: list[AssessmentResponse]


class TaskResponse(ApiModel):
    id: str
    project_id: str
    requirement_id: str | None
    title: str
    owner: str
    deadline: date | None
    status: str
    created_at: datetime


class AuditEventResponse(ApiModel):
    id: str
    project_id: str
    requirement_id: str | None
    action: str
    entity: str
    old_value: str
    new_value: str
    user: str = Field(validation_alias="actor")
    created_at: datetime


class WorkspaceResponse(ProjectResponse):
    source_documents: list[SourceDocumentResponse]
    evidence_documents: list[EvidenceDocumentResponse]
    requirements: list[RequirementResponse]
    tasks: list[TaskResponse]
    audit_events: list[AuditEventResponse]


class RequirementCreate(ApiModel):
    title: str = Field(default="", max_length=200)
    original_text: str = Field(min_length=1, max_length=20_000)
    category: str = Field(default="overig", max_length=80)
    priority: str = Field(default="verplicht", max_length=30)


class RequirementUpdate(ApiModel):
    title: str = Field(min_length=1, max_length=200)
    original_text: str = Field(min_length=1, max_length=20_000)
    category: str = Field(max_length=80)
    priority: str = Field(max_length=30)
    not_applicable: bool = False


class RequirementsMerge(ApiModel):
    primary_id: str
    secondary_id: str


class AssessmentUpsert(ApiModel):
    evidence_match_id: str | None = None
    status: str
    draft_answer: str = Field(default="", max_length=20_000)
    notes: str = Field(default="", max_length=20_000)
    owner: str = Field(default="", max_length=200)
    deadline: date | None = None
    approved: bool = False


class MutationResult(ApiModel):
    ok: bool = True
    count: int = 0
