# IPC UX-audit

## Hoofdconclusie

IPC moet voelen als een werkruimte voor een inhoudelijk team, niet als een AI-product dat probeert indruk te maken. De primaire route is daarom:

1. context van het dossier vastleggen;
2. bron en eisen controleren;
3. bewijsvoorstellen bekijken;
4. menselijke beoordeling vastleggen;
5. hiaten als acties opvolgen;
6. pas daarna exporteren.

## Wat is aangepast

- Het nieuwe-dossierformulier is verdeeld in `Dossieridentiteit`, `Productscope` en `Eigenaarschap`.
- De matrix opent met een samenvatting van menselijke voortgang, hiaten en voorstellen.
- De matrix-instructie gebruikt de inhoudelijke volgorde: bronfragment → voorstel → beoordeling.
- Het beoordelingspaneel is een gewone uitklapbare rij in plaats van een schermbrede overlay. Daardoor blijft navigatie altijd bereikbaar en werkt de flow ook met toetsenbord en kleine schermen.
- Er is een aparte Pages-browserdemo, maar die maakt expliciet onderscheid met de echte backend-MVP.
- Statuskleuren, bronteksten en waarschuwingen blijven semantisch; automatische scores worden nooit als beslissing gepresenteerd.

## Anti-AI-slop beslissingen

- Geen paarse/neon-gradienten, decoratieve AI-labels of generieke “next-gen”-copy.
- Geen losse nummering als decoratie; een nummer verschijnt alleen wanneer het een echte stap of dossieridentiteit verduidelijkt.
- Geen drie gelijke marketingkaarten als hoofdstructuur.
- Geen animatie die betekenis moet vervangen. Interactie is functioneel: openen, filteren, beoordelen, exporteren.
- Specifieke Nederlandse demo-inhoud, echte foutpaden en bewuste hiaten in plaats van gladde succesclaims.

## Onderzoek als kwalitatieve input

Reddit-discussies zijn gebruikt als signalering, niet als formele UX-standaard. Terugkerende observaties waren: generieke hero-plus-kaartenstructuren, paarse gradients, overmatig afgeronde pillen, decoratieve `01/02/03`-stappen, onduidelijke gebruikersroutes en knoppen die niets doen. De relevante correctie voor IPC is niet “er anders uitzien om anders te zijn”, maar de interface laten volgen uit het echte bewijsproces.

## Open meetpunten voor de volgende iteratie

- Test met drie rollen: dossierbeheerder, inhoudelijk eigenaar en sales/tender.
- Meet tijd tot eerste bruikbare beoordeling, aantal terugklikken en percentage eisen met bronfragment.
- Observeer vooral de eerste vijf minuten: begrijpt iemand waar te beginnen, waarom een voorstel niet definitief is en wat de volgende actie is?
- Voeg pas daarna nieuwe functies toe; geen extra dashboards voordat de matrixflow aantoonbaar soepel is.
