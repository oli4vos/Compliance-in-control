from datetime import date, timedelta

from fastapi.testclient import TestClient


def create_project(client: TestClient) -> str:
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "Migratiedossier",
            "client": "Fictieve Organisatie",
            "product": "Controlebox",
            "productVersion": "3.0",
        },
    )
    assert response.status_code == 201
    return str(response.json()["id"])


def test_complete_workspace_workflow_uses_python_storage(client: TestClient) -> None:
    project_id = create_project(client)

    source = client.post(
        f"/api/v1/projects/{project_id}/source-documents",
        data={"type": "programma van eisen"},
        files={
            "file": (
                "uitvraag.txt",
                b"De leverancier moet persoonsgegevens tijdens transport versleutelen.",
                "text/plain",
            )
        },
    )
    assert source.status_code == 201
    assert source.json()["extractedText"].startswith("De leverancier")

    extracted = client.post(
        f"/api/v1/projects/{project_id}/source-documents/{source.json()['id']}/extract"
    )
    assert extracted.status_code == 200
    assert extracted.json()["count"] == 1

    expires_at = (date.today() - timedelta(days=1)).isoformat()
    evidence = client.post(
        f"/api/v1/projects/{project_id}/evidence-documents",
        data={
            "title": "Encryptiebeleid",
            "documentType": "beleidsdocument",
            "product": "Controlebox",
            "productVersion": "3.0",
            "expiresAt": expires_at,
            "tags": "encryptie beveiliging",
        },
        files={
            "file": (
                "bewijs.txt",
                b"Persoonsgegevens zijn met AES-256 versleuteld en transport gebruikt TLS 1.3.",
                "text/plain",
            )
        },
    )
    assert evidence.status_code == 201
    assert evidence.json()["expiresAt"] == expires_at

    matches = client.post(f"/api/v1/projects/{project_id}/matches/generate")
    assert matches.status_code == 200
    assert matches.json()["count"] >= 1

    workspace = client.get(f"/api/v1/projects/{project_id}/workspace").json()
    requirement = workspace["requirements"][0]
    proposal = requirement["matches"][0]
    assert proposal["fragment"]
    assert "verlopen" in proposal["warnings"]
    assert requirement["status"] == "niet beoordeeld"

    assessment = client.put(
        f"/api/v1/projects/{project_id}/requirements/{requirement['id']}/assessment",
        json={
            "evidenceMatchId": proposal["id"],
            "status": "voldoende onderbouwd",
            "draftAnswer": "Gecontroleerd door de eigenaar.",
            "owner": "Eva de Vries",
            "deadline": date.today().isoformat(),
            "approved": True,
        },
    )
    assert assessment.status_code == 200

    final_workspace = client.get(f"/api/v1/projects/{project_id}/workspace").json()
    assert final_workspace["requirements"][0]["status"] == "voldoende onderbouwd"
    assert final_workspace["sufficientCount"] == 1
    assert final_workspace["progress"] == 100
    assert final_workspace["tasks"][0]["status"] == "afgerond"

    csv_export = client.get(f"/api/v1/projects/{project_id}/export.csv")
    assert csv_export.status_code == 200
    assert "Encryptiebeleid" in csv_export.text
    assert "geen juridisch oordeel" in csv_export.text


def test_rejects_unsupported_or_oversized_upload(client: TestClient) -> None:
    project_id = create_project(client)
    unsupported = client.post(
        f"/api/v1/projects/{project_id}/source-documents",
        data={"type": "overig"},
        files={"file": ("script.html", b"<script>alert(1)</script>", "text/html")},
    )
    assert unsupported.status_code == 415
