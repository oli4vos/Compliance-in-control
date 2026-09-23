from datetime import date, timedelta
from io import BytesIO
from pathlib import Path

import pytest
from docx import Document
from fastapi.testclient import TestClient
from pypdf import PdfWriter

from app.core.config import get_settings


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


def test_rejects_unsupported_or_oversized_upload(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    project_id = create_project(client)
    unsupported = client.post(
        f"/api/v1/projects/{project_id}/source-documents",
        data={"type": "overig"},
        files={"file": ("script.html", b"<script>alert(1)</script>", "text/html")},
    )
    assert unsupported.status_code == 415

    monkeypatch.setattr(get_settings(), "max_upload_bytes", 4)
    oversized = client.post(
        f"/api/v1/projects/{project_id}/source-documents",
        data={"type": "overig"},
        files={"file": ("notulen.txt", b"vijf!", "text/plain")},
    )
    assert oversized.status_code == 413


def test_rejects_disguised_or_mismatched_upload(client: TestClient) -> None:
    project_id = create_project(client)
    disguised = client.post(
        f"/api/v1/projects/{project_id}/source-documents",
        data={"type": "overig"},
        files={"file": ("notulen.txt", b"%PDF-1.7\n", "text/plain")},
    )
    assert disguised.status_code == 415
    assert "TXT" in disguised.json()["detail"]

    mismatched = client.post(
        f"/api/v1/projects/{project_id}/source-documents",
        data={"type": "overig"},
        files={"file": ("notulen.txt", b"Veilige platte tekst", "application/pdf")},
    )
    assert mismatched.status_code == 415
    assert "niet overeen" in mismatched.json()["detail"]


def test_accepts_and_extracts_valid_docx(client: TestClient) -> None:
    project_id = create_project(client)
    stream = BytesIO()
    document = Document()
    document.add_paragraph("De leverancier moet toegang tot productieomgevingen beperken.")
    document.save(stream)

    response = client.post(
        f"/api/v1/projects/{project_id}/source-documents",
        data={"type": "programma van eisen"},
        files={
            "file": (
                "eisen.docx",
                stream.getvalue(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )
    assert response.status_code == 201
    assert "productieomgevingen beperken" in response.json()["extractedText"]
    assert response.json()["mimeType"].endswith("wordprocessingml.document")


def test_accepts_valid_pdf_structure(client: TestClient) -> None:
    project_id = create_project(client)
    stream = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)
    writer.write(stream)

    response = client.post(
        f"/api/v1/projects/{project_id}/source-documents",
        data={"type": "privacybijlage"},
        files={"file": ("bijlage.pdf", stream.getvalue(), "application/pdf")},
    )
    assert response.status_code == 201
    assert response.json()["mimeType"] == "application/pdf"
    assert "[[Pagina 1]]" in response.json()["extractedText"]


def test_removes_file_when_database_registration_fails(
    client: TestClient, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project_id = create_project(client)

    def fail_registration(*args: object, **kwargs: object) -> None:
        raise RuntimeError("gesimuleerde databasefout")

    monkeypatch.setattr(
        "app.api.v1.projects.create_source_document",
        fail_registration,
    )
    with pytest.raises(RuntimeError, match="gesimuleerde databasefout"):
        client.post(
            f"/api/v1/projects/{project_id}/source-documents",
            data={"type": "overig"},
            files={"file": ("notulen.txt", b"Geldige tekstinhoud", "text/plain")},
        )

    assert not list(tmp_path.rglob("*"))
