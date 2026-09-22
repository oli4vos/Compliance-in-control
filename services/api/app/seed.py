from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.config import get_settings
from app.database import SessionLocal
from app.modules.projects.models import AuditEvent, Project, ProjectMetrics

DEMO_PROJECT_ID = "demo-waterdam"


def seed_demo() -> None:
    if not get_settings().auto_seed_demo:
        return

    with SessionLocal() as session:
        existing = session.scalar(
            select(Project)
            .options(joinedload(Project.metrics))
            .where(Project.id == DEMO_PROJECT_ID)
        )
        if existing:
            return

        project = Project(
            id=DEMO_PROJECT_ID,
            name="AI-planningssoftware Gemeente Waterdam",
            client="Gemeente Waterdam",
            reference="WD-2026-041",
            due_date=date(2026, 11, 16),
            product="Planwijzer AI",
            product_version="2.3",
            owner="Eva de Vries",
            notes="Fictief demonstratiedossier voor een Europese aanbesteding.",
        )
        project.metrics = ProjectMetrics(
            requirement_count=11,
            reviewed_count=10,
            sufficient_count=4,
            missing_count=3,
            next_deadline=date(2026, 10, 15),
        )
        session.add(project)
        session.flush()
        session.add(
            AuditEvent(
                project_id=project.id,
                action="Demodossier geladen",
                entity=f"Project:{project.id}",
                new_value="Synthetische projectprojectie",
                actor="Systeem",
            )
        )
        session.commit()


if __name__ == "__main__":
    seed_demo()
