"""Move the complete evidence workspace to PostgreSQL.

Revision ID: 20260922_0002
Revises: 20260922_0001
Create Date: 2026-09-22
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260922_0002"
down_revision: str | None = "20260922_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "source_documents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("stored_name", sa.String(255), nullable=False),
        sa.Column("type", sa.String(80), nullable=False),
        sa.Column("mime_type", sa.String(120), nullable=False),
        sa.Column("extracted_text", sa.Text(), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_source_documents_project_id", "source_documents", ["project_id"])
    op.create_table(
        "requirements",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), nullable=False),
        sa.Column("source_document_id", sa.String(36), nullable=True),
        sa.Column("number", sa.String(30), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("original_text", sa.Text(), nullable=False),
        sa.Column("category", sa.String(80), nullable=False),
        sa.Column("source_location", sa.String(160), nullable=False),
        sa.Column("source_fragment", sa.Text(), nullable=False),
        sa.Column("priority", sa.String(30), nullable=False),
        sa.Column("origin", sa.String(30), nullable=False),
        sa.Column("status", sa.String(60), nullable=False),
        sa.Column("not_applicable", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["source_document_id"], ["source_documents.id"], ondelete="SET NULL"
        ),
        sa.UniqueConstraint("project_id", "number"),
    )
    op.create_index("ix_requirements_project_id", "requirements", ["project_id"])
    op.create_index("ix_requirements_status", "requirements", ["status"])
    op.create_table(
        "evidence_documents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("document_type", sa.String(80), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("organization", sa.String(200), nullable=False),
        sa.Column("product", sa.String(200), nullable=False),
        sa.Column("product_version", sa.String(100), nullable=False),
        sa.Column("environment", sa.String(100), nullable=False),
        sa.Column("owner", sa.String(200), nullable=False),
        sa.Column("issued_at", sa.Date(), nullable=True),
        sa.Column("expires_at", sa.Date(), nullable=True),
        sa.Column("confidentiality", sa.String(80), nullable=False),
        sa.Column("tags", sa.Text(), nullable=False),
        sa.Column("file_name", sa.String(255), nullable=False),
        sa.Column("stored_name", sa.String(255), nullable=False),
        sa.Column("mime_type", sa.String(120), nullable=False),
        sa.Column("extracted_text", sa.Text(), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_evidence_documents_project_id", "evidence_documents", ["project_id"])
    op.create_table(
        "evidence_matches",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("requirement_id", sa.String(36), nullable=False),
        sa.Column("evidence_document_id", sa.String(36), nullable=False),
        sa.Column("fragment", sa.Text(), nullable=False),
        sa.Column("source_location", sa.String(160), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("warnings", sa.Text(), nullable=False),
        sa.Column("proposal_status", sa.String(60), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["requirement_id"], ["requirements.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["evidence_document_id"], ["evidence_documents.id"], ondelete="CASCADE"
        ),
        sa.UniqueConstraint("requirement_id", "evidence_document_id"),
    )
    op.create_index("ix_evidence_matches_requirement_id", "evidence_matches", ["requirement_id"])
    op.create_index(
        "ix_evidence_matches_evidence_document_id", "evidence_matches", ["evidence_document_id"]
    )
    op.create_table(
        "assessments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("requirement_id", sa.String(36), nullable=False),
        sa.Column("evidence_match_id", sa.String(36), nullable=True, unique=True),
        sa.Column("status", sa.String(60), nullable=False),
        sa.Column("draft_answer", sa.Text(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("owner", sa.String(200), nullable=False),
        sa.Column("deadline", sa.Date(), nullable=True),
        sa.Column("approved", sa.Boolean(), nullable=False),
        sa.Column("assessed_by", sa.String(200), nullable=False),
        sa.Column("assessed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["requirement_id"], ["requirements.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["evidence_match_id"], ["evidence_matches.id"], ondelete="SET NULL"
        ),
    )
    op.create_index("ix_assessments_requirement_id", "assessments", ["requirement_id"])
    op.create_table(
        "tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("project_id", sa.String(36), nullable=False),
        sa.Column("requirement_id", sa.String(36), nullable=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("owner", sa.String(200), nullable=False),
        sa.Column("deadline", sa.Date(), nullable=True),
        sa.Column("status", sa.String(40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["requirement_id"], ["requirements.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_tasks_project_id", "tasks", ["project_id"])
    op.create_index("ix_tasks_requirement_id", "tasks", ["requirement_id"])
    op.add_column("audit_events", sa.Column("requirement_id", sa.String(36), nullable=True))
    op.create_foreign_key(
        "fk_audit_events_requirement_id",
        "audit_events",
        "requirements",
        ["requirement_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_audit_events_requirement_id", "audit_events", type_="foreignkey")
    op.drop_column("audit_events", "requirement_id")
    op.drop_table("tasks")
    op.drop_table("assessments")
    op.drop_table("evidence_matches")
    op.drop_table("evidence_documents")
    op.drop_table("requirements")
    op.drop_table("source_documents")
