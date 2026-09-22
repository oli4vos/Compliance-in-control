# GitHub en live testen

## Belangrijk over GitHub Pages

GitHub Pages serveert alleen statische HTML, CSS en JavaScript. Aantoonbaar is geen statische site: de app gebruikt een Next.js-frontend, een Python/FastAPI-backend, PostgreSQL en private bestandsverwerking. Daardoor kan de volledige MVP niet rechtstreeks op GitHub Pages draaien.

## Aanbevolen route

- GitHub: broncode, pull requests en CI.
- Een Node-host of container: de Next.js-frontend en dunne BFF.
- Een Python-container: de FastAPI-backend en later de workers.
- PostgreSQL en private objectopslag in de EU/EER.

De workflow in `.github/workflows/ci.yml` controleert op iedere push en pull request TypeScript, Python, Pytest, Alembic tegen PostgreSQL, het OpenAPI-contract, tests en de productiebuild.

Voor lokaal testen:

```bash
npm install
npm run dev:stack
```

## Als GitHub Pages verplicht is

Maak dan een aparte statische investor-site of product-marketingpagina. De interactieve dossier-MVP blijft op de Next.js- en FastAPI-hosting. De statische variant mag geen claims doen over werkende uploads, matching of gegevensopslag als die backend niet beschikbaar is.

## Eerste GitHub-stappen

```bash
git init -b main
git add .
git commit -m "Initial Aantoonbaar MVP"
git remote add origin https://github.com/<organisatie>/<repository>.git
git push -u origin main
```

Vervang de placeholder-URL door de echte GitHub-repository. Exporteer geen `.env`, databasebestanden of `storage/uploads/` naar GitHub.
