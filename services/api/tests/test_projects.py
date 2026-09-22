from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.projects.models import AuditEvent, Project


def test_health_and_readiness(client: TestClient) -> None:
    assert client.get("/health").json()["status"] == "ok"
    assert client.get("/ready").json()["status"] == "ready"


def test_create_and_list_project_with_audit(client: TestClient, session: Session) -> None:
    response = client.post(
        "/api/v1/projects",
        headers={"Idempotency-Key": "project-waterdam-1"},
        json={
            "name": "AI-planningssoftware Gemeente Waterdam",
            "client": "Gemeente Waterdam",
            "reference": "WD-2026-041",
            "dueDate": "2026-11-16",
            "product": "Planwijzer AI",
            "productVersion": "2.3",
            "owner": "Eva de Vries",
            "notes": "API-test",
        },
    )
    assert response.status_code == 201
    project = response.json()
    assert project["name"] == "AI-planningssoftware Gemeente Waterdam"
    assert project["progress"] == 0

    duplicate = client.post(
        "/api/v1/projects",
        headers={"Idempotency-Key": "project-waterdam-1"},
        json={"name": "Genegeerd", "client": "Genegeerd"},
    )
    assert duplicate.json()["id"] == project["id"]
    assert session.scalar(select(func.count()).select_from(Project)) == 1
    assert session.scalar(select(func.count()).select_from(AuditEvent)) == 1

    listed = client.get("/api/v1/projects")
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == project["id"]

    detail = client.get(f"/api/v1/projects/{project['id']}")
    assert detail.status_code == 200
    assert detail.json()["reference"] == "WD-2026-041"


def test_project_validation_is_dutch_ready(client: TestClient) -> None:
    response = client.post("/api/v1/projects", json={"name": "", "client": ""})
    assert response.status_code == 422
