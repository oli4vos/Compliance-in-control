# ruff: noqa: E501
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from app.core.config import get_settings
from app.database import SessionLocal
from app.modules.projects.matching import match_evidence
from app.modules.projects.models import (
    Assessment,
    AuditEvent,
    EvidenceDocument,
    EvidenceMatch,
    Project,
    ProjectMetrics,
    Requirement,
    SourceDocument,
    Task,
)
from app.modules.projects.workspace import refresh_metrics

DEMO_PROJECT_ID = "demo-waterdam"
REQUIREMENTS = [
    (
        "E-001",
        "Encryptie van gegevens",
        "De leverancier moet persoonsgegevens tijdens transport en opslag versleutelen met actuele, algemeen aanvaarde cryptografische standaarden.",
        "informatiebeveiliging",
        "§ 4.1",
    ),
    (
        "E-002",
        "Toegangsbeheer",
        "De opdrachtnemer waarborgt rolgebaseerd toegangsbeheer en voert ieder kwartaal een toegangsreview uit.",
        "informatiebeveiliging",
        "§ 4.2",
    ),
    (
        "E-003",
        "Controleerbare logging",
        "Het AI-systeem dient beheerdershandelingen en relevante gebruikersacties controleerbaar te loggen.",
        "informatiebeveiliging",
        "§ 4.3",
    ),
    (
        "E-004",
        "Bewaartermijnen",
        "De inschrijver toont aan dat persoonsgegevens na afloop van de overeengekomen bewaartermijn worden verwijderd.",
        "privacy",
        "§ 5.1",
    ),
    (
        "E-005",
        "Subverwerkers",
        "De leverancier beschrijft alle subverwerkers, hun locaties en het doel van verwerking.",
        "privacy",
        "§ 5.2",
    ),
    (
        "E-006",
        "Incidentmelding",
        "Beveiligingsincidenten met mogelijke impact op de opdrachtgever moeten binnen 24 uur worden gemeld.",
        "informatiebeveiliging",
        "§ 4.6",
    ),
    (
        "E-007",
        "Menselijke tussenkomst",
        "Bij besluiten met aanmerkelijke gevolgen moet betekenisvolle menselijke tussenkomst mogelijk zijn.",
        "AI en algoritmen",
        "§ 6.1",
    ),
    (
        "E-008",
        "Uitleg algoritmische uitkomsten",
        "De leverancier dient begrijpelijk uit te leggen welke factoren een algoritmische uitkomst hoofdzakelijk bepalen.",
        "AI en algoritmen",
        "§ 6.2",
    ),
    (
        "E-009",
        "Wijzigingen van het AI-model",
        "De opdrachtgever moet vooraf worden geïnformeerd over materiële wijzigingen van het gebruikte AI-model.",
        "AI en algoritmen",
        "§ 6.4",
    ),
    (
        "E-010",
        "Continuïteit en herstel",
        "De inschrijver toont aan dat continuïteits- en herstelprocedures minimaal jaarlijks worden getest.",
        "continuïteit",
        "§ 7.1",
    ),
    (
        "E-011",
        "Opslag binnen de EER",
        "Persoonsgegevens moeten uitsluitend binnen de Europese Economische Ruimte worden opgeslagen.",
        "privacy",
        "§ 5.4",
    ),
]
EVIDENCE = [
    dict(
        title="Informatiebeveiligingsbeleid 2026",
        document_type="beleidsdocument",
        description="Kaders voor encryptie, toegangsbeheer en logging.",
        organization="Planwijzer Systemen B.V.",
        product="Planwijzer AI",
        product_version="2.3",
        environment="productie",
        owner="Nora Smit",
        issued_at=date(2026, 2, 1),
        expires_at=date(2027, 2, 1),
        confidentiality="intern",
        tags="encryptie, toegangsbeheer, logging",
        file_name="informatiebeveiligingsbeleid.txt",
        stored_name="demo-security.txt",
        mime_type="text/plain",
        extracted_text="Gegevens worden tijdens transport beschermd met TLS 1.3 en in opslag met AES-256. Toegang is rolgebaseerd en ieder kwartaal beoordeelt de systeemeigenaar de toegekende rechten. Beheerdershandelingen worden onveranderbaar gelogd en twaalf maanden bewaard.",
    ),
    dict(
        title="Subprocessorregister",
        document_type="register",
        description="Actuele lijst van subverwerkers en verwerkingslocaties.",
        organization="Planwijzer Systemen B.V.",
        product="Planwijzer AI",
        product_version="2.3",
        environment="productie",
        owner="Mila van Dijk",
        issued_at=date(2026, 8, 12),
        expires_at=None,
        confidentiality="vertrouwelijk",
        tags="subverwerkers, EER, locaties",
        file_name="subprocessorregister.txt",
        stored_name="demo-subprocessors.txt",
        mime_type="text/plain",
        extracted_text="Rekenwolk Noord B.V. verzorgt hosting in Amsterdam, Nederland. Berichtstroom B.V. verzorgt e-mailaflevering in Frankfurt, Duitsland. Alle productiegegevens worden binnen de EER verwerkt en opgeslagen.",
    ),
    dict(
        title="Architectuurbeschrijving Planwijzer AI",
        document_type="architectuurdiagram",
        description="Technische componenten en gegevensstromen.",
        organization="Planwijzer Systemen B.V.",
        product="Planwijzer AI",
        product_version="2.2",
        environment="productie",
        owner="Sven Meijer",
        issued_at=date(2026, 1, 18),
        expires_at=None,
        confidentiality="vertrouwelijk",
        tags="architectuur, encryptie, logging",
        file_name="architectuurbeschrijving.txt",
        stored_name="demo-architecture.txt",
        mime_type="text/plain",
        extracted_text="De applicatie gebruikt een versleutelde database in de regio West-Europa. Auditgebeurtenissen gaan naar een afgescheiden logopslag. Dit document beschrijft versie 2.2 en is nog niet bijgewerkt voor de nieuwe planningsmodule.",
    ),
    dict(
        title="Procedure beveiligingsincidenten",
        document_type="procedure",
        description="Melding, triage en escalatie van incidenten.",
        organization="Planwijzer Systemen B.V.",
        product="Organisatiebreed",
        product_version="",
        environment="productie",
        owner="Nora Smit",
        issued_at=date(2026, 4, 4),
        expires_at=date(2027, 4, 4),
        confidentiality="intern",
        tags="incident, melding, 24 uur",
        file_name="incidentprocedure.txt",
        stored_name="demo-incidents.txt",
        mime_type="text/plain",
        extracted_text="Een incident met mogelijke impact op een opdrachtgever wordt direct geëscaleerd. De contracteigenaar doet uiterlijk binnen 24 uur een eerste melding met aard, impact en genomen maatregelen.",
    ),
    dict(
        title="Model card Planwijzer voorspeller",
        document_type="technische beschrijving",
        description="Doel, beperkingen en uitlegbaarheid van het planningsmodel.",
        organization="Planwijzer Systemen B.V.",
        product="Planwijzer AI",
        product_version="2.3",
        environment="productie",
        owner="Ravi de Boer",
        issued_at=date(2026, 7, 9),
        expires_at=None,
        confidentiality="intern",
        tags="AI, model, uitleg, menselijke controle",
        file_name="model-card.txt",
        stored_name="demo-model-card.txt",
        mime_type="text/plain",
        extracted_text="Het model rangschikt planningsopties op reistijd, beschikbaarheid en urgentie. Een planner ziet de drie zwaarst wegende factoren en kan iedere aanbeveling negeren of aanpassen. Besluiten worden nooit zonder bevestiging van een planner uitgevoerd. Wijzigingen worden intern getest.",
    ),
    dict(
        title="Continuïteits- en herstelplan",
        document_type="procedure",
        description="Herstelvolgorde, rollen en testcyclus.",
        organization="Planwijzer Systemen B.V.",
        product="Planwijzer AI",
        product_version="2.3",
        environment="productie",
        owner="Iris de Jong",
        issued_at=date(2026, 3, 20),
        expires_at=date(2027, 3, 20),
        confidentiality="strikt vertrouwelijk",
        tags="continuïteit, herstel, test",
        file_name="continuiteitsplan.txt",
        stored_name="demo-bcp.txt",
        mime_type="text/plain",
        extracted_text="Het herstelplan beschrijft rollen, afhankelijkheden en een herstelvolgorde. Een volledige hersteltest vindt jaarlijks plaats; de laatste oefening was op 14 februari 2026 en is vastgelegd in een afzonderlijk testrapport.",
    ),
    dict(
        title="Pentestsamenvatting 2024",
        document_type="testresultaat",
        description="Samenvatting van een externe penetratietest op een oudere versie.",
        organization="Planwijzer Labs B.V.",
        product="Planwijzer AI",
        product_version="1.9",
        environment="test",
        owner="Nora Smit",
        issued_at=date(2024, 5, 10),
        expires_at=date(2025, 5, 10),
        confidentiality="vertrouwelijk",
        tags="pentest, beveiliging",
        file_name="pentest-samenvatting.txt",
        stored_name="demo-pentest.txt",
        mime_type="text/plain",
        extracted_text="De testomgeving van versie 1.9 is onderzocht op veelvoorkomende kwetsbaarheden. Twee bevindingen met gemiddeld risico zijn na afloop hertest.",
    ),
]
STATUSES = {
    "E-001": "voldoende onderbouwd",
    "E-002": "gedeeltelijk onderbouwd",
    "E-003": "mogelijk passend",
    "E-004": "ontbrekend bewijs",
    "E-005": "voldoende onderbouwd",
    "E-006": "voldoende onderbouwd",
    "E-007": "gedeeltelijk onderbouwd",
    "E-008": "gedeeltelijk onderbouwd",
    "E-009": "onvoldoende onderbouwd",
    "E-010": "voldoende onderbouwd",
    "E-011": "onvoldoende onderbouwd",
}


def seed_demo() -> None:
    if not get_settings().auto_seed_demo:
        return
    with SessionLocal() as session:
        project = session.scalar(
            select(Project)
            .where(Project.id == DEMO_PROJECT_ID)
            .options(
                joinedload(Project.metrics),
                selectinload(Project.source_documents),
                selectinload(Project.requirements),
                selectinload(Project.evidence_documents),
                selectinload(Project.tasks),
            )
        )
        if project and project.source_documents:
            return
        if project is None:
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
            project.metrics = ProjectMetrics()
            session.add(project)
            session.flush()
        source = SourceDocument(
            project_id=project.id,
            name="Programma van Eisen Waterdam.txt",
            stored_name="demo-pve.txt",
            type="programma van eisen",
            mime_type="text/plain",
            extracted_text="\n\n".join(f"{item[4]} {item[2]}" for item in REQUIREMENTS),
        )
        ai_source = SourceDocument(
            project_id=project.id,
            name="AI- en privacyvragenlijst Waterdam.txt",
            stored_name="demo-ai-vragenlijst.txt",
            type="AI-vragenlijst",
            mime_type="text/plain",
            extracted_text="\n\n".join(f"{item[4]} {item[2]}" for item in REQUIREMENTS[3:9]),
        )
        session.add_all([source, ai_source])
        session.flush()
        ai_numbers = {"E-004", "E-005", "E-007", "E-008", "E-009", "E-011"}
        requirements = [
            Requirement(
                project_id=project.id,
                source_document_id=ai_source.id if number in ai_numbers else source.id,
                number=number,
                title=title,
                original_text=text,
                category=category,
                source_location=location,
                source_fragment=text,
                priority="verplicht",
                origin="automatisch",
                status=STATUSES[number],
            )
            for number, title, text, category, location in REQUIREMENTS
        ]
        evidence = [EvidenceDocument(project_id=project.id, **item) for item in EVIDENCE]
        session.add_all(requirements)
        session.add_all(evidence)
        session.flush()
        for requirement in requirements:
            for proposal in match_evidence(requirement, evidence, project):
                session.add(
                    EvidenceMatch(
                        requirement_id=requirement.id,
                        evidence_document_id=proposal.evidence_document_id,
                        fragment=proposal.fragment,
                        source_location=proposal.source_location,
                        score=proposal.score,
                        explanation=proposal.explanation,
                        warnings=proposal.warnings,
                    )
                )
            deadline = (
                date(2026, 10, 15) if requirement.number in {"E-004", "E-009", "E-011"} else None
            )
            owner = (
                "Mila van Dijk"
                if requirement.category == "privacy"
                else "Ravi de Boer"
                if requirement.category == "AI en algoritmen"
                else "Nora Smit"
            )
            session.add(
                Assessment(
                    requirement_id=requirement.id,
                    status=requirement.status,
                    draft_answer="Nog op te stellen antwoord."
                    if requirement.status == "ontbrekend bewijs"
                    else "Zie gekoppelde bewijsstukken en bronfragmenten.",
                    notes="Aanvullend, scopespecifiek bewijs opvragen."
                    if deadline
                    else "Menselijk gecontroleerd in de demo.",
                    owner=owner,
                    deadline=deadline,
                    approved=requirement.status == "voldoende onderbouwd",
                )
            )
            if deadline:
                task = Task(
                    project_id=project.id,
                    requirement_id=requirement.id,
                    title=f"Beoordeling afronden voor {requirement.number}",
                    owner=owner,
                    deadline=deadline,
                )
                project.tasks.append(task)
                session.add(task)
        project.requirements = requirements
        refresh_metrics(project)
        session.add(
            AuditEvent(
                project_id=project.id,
                action="Demodossier geladen",
                entity=f"Project:{project.id}",
                new_value="Synthetische Python/PostgreSQL-demo-inhoud",
                actor="Systeem",
            )
        )
        session.commit()


if __name__ == "__main__":
    seed_demo()
