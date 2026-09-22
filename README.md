# Aantoonbaar

Aantoonbaar is een lokale MVP voor Nederlandse IT- en AI-leveranciers die eisen uit aanbestedingen, securityvragenlijsten en klantuitvragen willen koppelen aan controleerbare bewijsstukken. De app helpt bij ordenen en beoordelen; zij geeft geen juridisch oordeel, certificering of garantie van naleving.

De volledige technische samenhang, huidige risico's en productie-doelarchitectuur staan in [ARCHITECTURE.md](ARCHITECTURE.md).

## Technologie

- Next.js 16 met App Router en TypeScript
- React 19 en Tailwind CSS 4
- Prisma 6 met SQLite
- Lokale, niet-publieke bestandsopslag in `storage/uploads/`
- Lokale heuristische extractie en matching
- Optionele OpenAI Responses API-adapters met automatische lokale terugval
- Vitest en Playwright

## Installeren en starten

Vereisten: Node.js 20+ en npm.

```bash
npm install
npm run db:setup
npm run seed
npm run dev
```

Open daarna [http://localhost:3000](http://localhost:3000). `npm run db:setup` maakt de lokale SQLite-database aan en synchroniseert het schema. `npm run seed` laadt het fictieve Waterdam-demodossier opnieuw; een bestaand demodossier met referentie `WD-2026-041` wordt daarbij vervangen.

## Beschikbare opdrachten

```bash
npm run dev          # ontwikkelserver op localhost:3000
npm run build        # productiebuild en TypeScript-controle
npm run db:setup     # Prisma-client genereren en SQLite-schema synchroniseren
npm run seed         # synthetische demo-data laden
npm test             # unit- en domeintests
npm run test:e2e     # Playwright end-to-endtest
npm run typecheck    # alleen TypeScript-controle
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

## Bekende beperkingen

- PDF-paginareferenties zijn afhankelijk van wat de PDF-parser betrouwbaar kan uitlezen; DOCX en TXT gebruiken alineareferenties.
- De lokale matcher gebruikt trefwoorden en tekstoverlap, geen semantische vectorzoekmachine.
- Demo-documenten bestaan als database-inhoud; hun fictieve bronbestanden worden niet op schijf gezet.
- Bewijs kan via de beveiligde route worden gedownload, maar er is nog geen inline documentviewer.
- Het auditlog is eenvoudig en lokaal, niet onveranderbaar of cryptografisch ondertekend.
- Fouten van serveracties gebruiken nog de standaard Next.js-foutafhandeling; productie vraagt om veldspecifieke foutmeldingen en monitoring.

## Vervolg richting productie

1. Voeg organisatie- en rolgebaseerde authenticatie, autorisatie en tenantisolatie toe.
2. Introduceer versleutelde objectopslag, malware-scanning, back-ups en aantoonbaar retentiebeleid.
3. Voeg een documentviewer toe met robuuste paginacoördinaten en annotaties.
4. Maak auditlogs append-only en voeg review-/vier-ogenworkflows toe.
5. Voer securitytests, privacy-impactanalyse, toegankelijkheidsaudit en gecontroleerde deployment uit.
