# GitHub en live testen

## Belangrijk over GitHub Pages

GitHub Pages serveert alleen statische HTML, CSS en JavaScript. Aantoonbaar is in de huidige MVP geen statische site: de app gebruikt Next.js Server Actions, Prisma/SQLite, lokale bestandsextractie en uploads buiten `public/`. Daardoor kan de volledige MVP niet rechtstreeks op GitHub Pages draaien.

## Aanbevolen route

- GitHub: broncode, pull requests en CI.
- Een Node-host: de Next.js-app en serverfuncties.
- Een gedeelde database/object storage: zodra meerdere gebruikers of productiegegevens nodig zijn.

De workflow in `.github/workflows/ci.yml` controleert op iedere push en pull request de installatie, database-initialisatie, TypeScript, tests en productiebuild.

Voor lokaal testen:

```bash
npm install
npm run db:setup
npm run seed
npm run dev
```

## Als GitHub Pages verplicht is

Maak dan een aparte statische investor-site of product-marketingpagina. De interactieve dossier-MVP blijft op een Node-host. De statische variant mag geen claims doen over werkende uploads, matching of SQLite-opslag als die backend niet beschikbaar is.

## Eerste GitHub-stappen

```bash
git init -b main
git add .
git commit -m "Initial Aantoonbaar MVP"
git remote add origin https://github.com/<organisatie>/<repository>.git
git push -u origin main
```

Vervang de placeholder-URL door de echte GitHub-repository. Exporteer geen `.env`, databasebestanden of `storage/uploads/` naar GitHub.
