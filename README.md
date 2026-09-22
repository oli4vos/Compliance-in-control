# Aantoonbaar

Aantoonbaar is een lokale MVP voor Nederlandse IT- en AI-leveranciers die eisen uit aanbestedingen, securityvragenlijsten en klantuitvragen willen koppelen aan controleerbare bewijsstukken. De app helpt bij ordenen en beoordelen; zij geeft geen juridisch oordeel, certificering of garantie van naleving.

De volledige technische samenhang, huidige risico's en productie-doelarchitectuur staan in [ARCHITECTURE.md](ARCHITECTURE.md).

> **Architectuurbesluit:** de huidige MVP gebruikt nog Next.js Server Actions en Prisma als lokale backend. De vastgestelde doelarchitectuur gebruikt altijd een Python/FastAPI-backend; Next.js blijft de frontend. De migratievolgorde en grens tussen beide staan in de architectuurblauwdruk.

## Technologie

- Next.js 16 met App Router en TypeScript voor de frontend
- React 19 en Tailwind CSS 4
- Python/FastAPI, Pydantic, SQLAlchemy en Alembic voor de nieuwe backend
- PostgreSQL voor de gezaghebbende projectservice
- Prisma 6 met SQLite als tijdelijke compatibiliteitslaag voor nog niet gemigreerde modules
- Lokale, niet-publieke bestandsopslag in `storage/uploads/`
- Lokale heuristische extractie en matching
- Optionele OpenAI Responses API-adapters met automatische lokale terugval
- Vitest en Playwright

## Installeren en starten

Aanbevolen vereisten: Docker Desktop met Docker Compose. Start de volledige frontend, Python-API en PostgreSQL-database met één opdracht:

```bash
npm install
npm run dev:stack
```

Open daarna [http://localhost:3000](http://localhost:3000). De interactieve Python-API-documentatie staat op [http://localhost:8000/docs](http://localhost:8000/docs). Docker Compose voert de Alembic-migratie uit en laadt het fictieve Waterdam-demodossier in beide tijdelijke datalagen.

Omdat het project in een iCloud-map staat, gebruikt Compose bewust ingebouwde images en Docker named volumes in plaats van macOS bind-mounts. Na een codewijziging voert u opnieuw `npm run dev:stack` uit om de images bij te werken.

Stoppen kan met `Ctrl+C`; verwijder alleen de lokale containervolumes wanneer u bewust alle lokale PostgreSQL-data wilt wissen:

```bash
docker compose down
```

Voor ontwikkeling zonder Docker moeten PostgreSQL en de twee processen afzonderlijk worden gestart. Gebruik daarbij `PYTHON_API_URL=http://127.0.0.1:8000` voor Next.js en een geldige `AANTOONBAAR_DATABASE_URL` voor FastAPI.

## Beschikbare opdrachten

```bash
npm run dev          # ontwikkelserver op localhost:3000
npm run dev:stack    # volledige stack: Next.js, FastAPI en PostgreSQL
npm run build        # productiebuild en TypeScript-controle
npm run db:setup     # Prisma-client genereren en SQLite-schema synchroniseren
npm run seed         # synthetische demo-data laden
npm test             # unit- en domeintests
npm run test:e2e     # Playwright end-to-endtest
npm run typecheck    # alleen TypeScript-controle
npm run api:generate # TypeScript-typen opnieuw genereren uit OpenAPI
```

Python-controles:

```bash
python3 -m venv services/api/.venv
services/api/.venv/bin/pip install -e 'services/api[dev]'
services/api/.venv/bin/ruff check services/api
services/api/.venv/bin/mypy --config-file services/api/pyproject.toml services/api/app
services/api/.venv/bin/pytest services/api
```

Installeer vóór de eerste browsertest zo nodig Chromium met `npx playwright install chromium`.

## Kernworkflow

1. Maak een dossier aan.
2. Upload een PDF-, DOCX- of TXT-brondocument en classificeer het.
3. Genereer concept-eisen met bronfragmenten.
4. Bewerk, verwijder, combineer of voeg eisen handmatig toe.
5. Registreer bewijsstukken met scope, eigenaar, geldigheid en vertrouwelijkheid.
6. Genereer lokale bewijsvoorstellen en controleer fragmenten en waarschuwingen.
7. Leg een afzonderlijke menselijke beoordeling, eigenaar, deadline en goedkeuring vast.
8. Download de CSV-matrix of open het afdrukbare dossier en bewaar dit via de browser als PDF.

De voortgang gebruikt uitsluitend menselijke beoordelingsstatussen. Een automatische match wordt nooit automatisch `voldoende onderbouwd`.

## Optionele AI-configuratie

De app is zonder API-sleutel volledig bruikbaar. Kopieer optionele waarden uit `.env.example` naar `.env.local`:

```env
OPENAI_API_KEY="..."
OPENAI_MODEL="gpt-6-astra"
```

Met een sleutel worden de LLM-implementaties van `RequirementExtractor` en `EvidenceMatcher` geactiveerd. API-fouten vallen terug op de lokale implementaties. Pas `OPENAI_MODEL` aan als het gekozen model niet voor het account beschikbaar is. De integratie gebruikt de Responses API volgens de [officiële OpenAI-quickstart](https://developers.openai.com/api/docs/quickstart?site_locale=en). Let op: documenten die via deze optionele route worden verwerkt, verlaten de lokale omgeving en vallen onder de voorwaarden en gegevensinstellingen van de gekozen API-provider.

## Bestands- en gegevensveiligheid

- Alleen `.pdf`, `.docx` en `.txt` tot 10 MB worden geaccepteerd.
- Bestandsnamen en dossier-id's worden ontsmet; opgeslagen bestanden krijgen een willekeurige naam.
- Uploads staan niet in `public/` en zijn uitgesloten van Git.
- Een bestandsroute controleert altijd zowel project-id als document-id.
- Geüploade inhoud wordt niet als vertrouwde HTML gerenderd en niet naar de console geschreven.
- Secrets horen uitsluitend in `.env.local`; `.env*` en uploads staan in `.gitignore`.

Dit is een lokale MVP, geen productieklare beveiligingsomgeving. Er is één standaardgebruiker, geen authenticatie, geen encryptie-at-rest buiten wat het lokale besturingssysteem biedt, geen malware-scanning, geen fijnmazige autorisatie en geen back-up- of retentiebeleid. Gebruik geen echte vertrouwelijke aanbestedingsinformatie voordat deze maatregelen zijn toegevoegd.

## Tests

De tests dekken lokale eisenextractie, traceerbare matching, verlopen en binnenkort verlopend bewijs, CSV-escaping en de browserworkflow voor projectaanmaak, TXT-upload, extractie, bewijsregistratie, matching, menselijke status en export.

```bash
npm test
npm run test:e2e
```

De Playwright-configuratie start voor lokale tests zowel FastAPI als Next.js. De aanvullende E2E-test controleert dat een dossier via FastAPI wordt aangemaakt, rechtstreeks in de API terugkomt en op het dashboard verschijnt.

## Bekende beperkingen

- Alleen de projectlijst en projectaanmaak zijn al gezaghebbend naar Python/PostgreSQL gemigreerd. Documenten, eisen, bewijs, beoordelingen en exports gebruiken tijdelijk nog Prisma/SQLite.
- Nieuwe Python-projecten krijgen tijdens deze overgang een Prisma-projectie met hetzelfde id, zodat de bestaande volledige werkruimte blijft functioneren. Deze projectie wordt verwijderd na migratie van de documentmodule.
- PDF-paginareferenties zijn afhankelijk van wat de PDF-parser betrouwbaar kan uitlezen; DOCX en TXT gebruiken alineareferenties.
- De lokale matcher gebruikt trefwoorden en tekstoverlap, geen semantische vectorzoekmachine.
- Demo-documenten bestaan als database-inhoud; hun fictieve bronbestanden worden niet op schijf gezet.
- Bewijs kan via de beveiligde route worden gedownload, maar er is nog geen inline documentviewer.
- Het auditlog is eenvoudig en lokaal, niet onveranderbaar of cryptografisch ondertekend.
- Fouten van serveracties gebruiken nog de standaard Next.js-foutafhandeling; productie vraagt om veldspecifieke foutmeldingen en monitoring.

## Vervolg richting productie

1. Migreer documenten en private bestandsopslag als volgende verticale Python-slice.
2. Migreer eisen, bewijs, matching, beoordeling en export en verwijder daarna Prisma/SQLite.
3. Voeg organisatie- en rolgebaseerde authenticatie, ownership policies en tenantisolatie toe.
4. Introduceer versleutelde objectopslag, malware-scanning, back-ups en aantoonbaar retentiebeleid.
5. Voer securitytests, privacy-impactanalyse, toegankelijkheidsaudit en gecontroleerde deployment uit.
