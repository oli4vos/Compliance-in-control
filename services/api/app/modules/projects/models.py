from datetime import date, datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(200))
    client: Mapped[str] = mapped_column(String(200))
    reference: Mapped[str] = mapped_column(String(100), default="")
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    product: Mapped[str] = mapped_column(String(200), default="")
    product_version: Mapped[str] = mapped_column(String(100), default="")
    owner: Mapped[str] = mapped_column(String(200), default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    idempotency_key: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)

    metrics: Mapped["ProjectMetrics"] = relationship(
        back_populates="project", cascade="all, delete-orphan", uselist=False
    )
    source_documents: Mapped[list["SourceDocument"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    requirements: Mapped[list["Requirement"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    evidence_documents: Mapped[list["EvidenceDocument"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    audit_events: Mapped[list["AuditEvent"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class ProjectMetrics(Base):
    __tablename__ = "project_metrics"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    requirement_count: Mapped[int] = mapped_column(Integer, default=0)
    reviewed_count: Mapped[int] = mapped_column(Integer, default=0)
    sufficient_count: Mapped[int] = mapped_column(Integer, default=0)
    missing_count: Mapped[int] = mapped_column(Integer, default=0)
    next_deadline: Mapped[date | None] = mapped_column(Date, nullable=True)

    project: Mapped[Project] = relationship(back_populates="metrics")


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    requirement_id: Mapped[str | None] = mapped_column(
        ForeignKey("requirements.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(120))
    entity: Mapped[str] = mapped_column(String(120))
    old_value: Mapped[str] = mapped_column(Text, default="")
    new_value: Mapped[str] = mapped_column(Text, default="")
    actor: Mapped[str] = mapped_column(String(200), default="Lokale gebruiker")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    project: Mapped[Project] = relationship(back_populates="audit_events")


class SourceDocument(Base):
    __tablename__ = "source_documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(255))
    stored_name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(80))
    mime_type: Mapped[str] = mapped_column(String(120))
    extracted_text: Mapped[str] = mapped_column(Text)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    project: Mapped[Project] = relationship(back_populates="source_documents")
    requirements: Mapped[list["Requirement"]] = relationship(back_populates="source_document")


class Requirement(Base):
    __tablename__ = "requirements"
    __table_args__ = (UniqueConstraint("project_id", "number"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    source_document_id: Mapped[str | None] = mapped_column(
        ForeignKey("source_documents.id", ondelete="SET NULL"), nullable=True
    )
    number: Mapped[str] = mapped_column(String(30))
    title: Mapped[str] = mapped_column(String(200))
    original_text: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(80))
    source_location: Mapped[str] = mapped_column(String(160))
    source_fragment: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(30), default="verplicht")
    origin: Mapped[str] = mapped_column(String(30), default="automatisch")
    status: Mapped[str] = mapped_column(String(60), default="niet beoordeeld", index=True)
    not_applicable: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    project: Mapped[Project] = relationship(back_populates="requirements")
    source_document: Mapped[SourceDocument | None] = relationship(back_populates="requirements")
    matches: Mapped[list["EvidenceMatch"]] = relationship(
        back_populates="requirement", cascade="all, delete-orphan"
    )
    assessments: Mapped[list["Assessment"]] = relationship(
        back_populates="requirement", cascade="all, delete-orphan"
    )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="requirement", cascade="all, delete-orphan"
    )


class EvidenceDocument(Base):
    __tablename__ = "evidence_documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(255))
    document_type: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(Text, default="")
    organization: Mapped[str] = mapped_column(String(200), default="")
    product: Mapped[str] = mapped_column(String(200), default="")
    product_version: Mapped[str] = mapped_column(String(100), default="")
    environment: Mapped[str] = mapped_column(String(100), default="")
    owner: Mapped[str] = mapped_column(String(200), default="")
    issued_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    expires_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    confidentiality: Mapped[str] = mapped_column(String(80), default="intern")
    tags: Mapped[str] = mapped_column(Text, default="")
    file_name: Mapped[str] = mapped_column(String(255))
    stored_name: Mapped[str] = mapped_column(String(255))
    mime_type: Mapped[str] = mapped_column(String(120))
    extracted_text: Mapped[str] = mapped_column(Text)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    project: Mapped[Project] = relationship(back_populates="evidence_documents")
    matches: Mapped[list["EvidenceMatch"]] = relationship(
        back_populates="evidence_document", cascade="all, delete-orphan"
    )


class EvidenceMatch(Base):
    __tablename__ = "evidence_matches"
    __table_args__ = (UniqueConstraint("requirement_id", "evidence_document_id"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    requirement_id: Mapped[str] = mapped_column(
        ForeignKey("requirements.id", ondelete="CASCADE"), index=True
    )
    evidence_document_id: Mapped[str] = mapped_column(
        ForeignKey("evidence_documents.id", ondelete="CASCADE"), index=True
    )
    fragment: Mapped[str] = mapped_column(Text, default="")
    source_location: Mapped[str] = mapped_column(String(160), default="Geëxtraheerde tekst")
    score: Mapped[int] = mapped_column(Integer)
    explanation: Mapped[str] = mapped_column(Text)
    warnings: Mapped[str] = mapped_column(Text, default="")
    proposal_status: Mapped[str] = mapped_column(String(60), default="niet beoordeeld")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    requirement: Mapped[Requirement] = relationship(back_populates="matches")
    evidence_document: Mapped[EvidenceDocument] = relationship(back_populates="matches")
    assessment: Mapped["Assessment | None"] = relationship(back_populates="evidence_match")


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    requirement_id: Mapped[str] = mapped_column(
        ForeignKey("requirements.id", ondelete="CASCADE"), index=True
    )
    evidence_match_id: Mapped[str | None] = mapped_column(
        ForeignKey("evidence_matches.id", ondelete="SET NULL"), unique=True, nullable=True
    )
    status: Mapped[str] = mapped_column(String(60))
    draft_answer: Mapped[str] = mapped_column(Text, default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    owner: Mapped[str] = mapped_column(String(200), default="")
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    assessed_by: Mapped[str] = mapped_column(String(200), default="Lokale gebruiker")
    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )

    requirement: Mapped[Requirement] = relationship(back_populates="assessments")
    evidence_match: Mapped[EvidenceMatch | None] = relationship(back_populates="assessment")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    requirement_id: Mapped[str | None] = mapped_column(
        ForeignKey("requirements.id", ondelete="CASCADE"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(255))
    owner: Mapped[str] = mapped_column(String(200), default="")
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(40), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    project: Mapped[Project] = relationship(back_populates="tasks")
    requirement: Mapped[Requirement | None] = relationship(back_populates="tasks")
