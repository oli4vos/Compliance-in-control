import { test, expect } from "@playwright/test";

test("volledige kernworkflow", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Van uitvraag/ })).toBeVisible();
  await page.getByRole("link", { name: "Nieuw dossier", exact: true }).click();
  await page.getByLabel("Projectnaam *", { exact: true }).fill("E2E controledossier");
  await page.getByLabel("Opdrachtgever *", { exact: true }).fill("Stichting Proeftuin");
  await page.getByLabel("Aangeboden product of dienst", { exact: true }).fill("Controlebox");
  await page.getByRole("button", { name: "Dossier aanmaken", exact: true }).click();
  await expect(page.getByRole("heading", { name: "E2E controledossier", exact: true })).toBeVisible();

  await page.getByRole("link", { name: "Aanbestedingsdocumenten", exact: true }).click();
  await page.getByLabel("Bestand *", { exact: true }).setInputFiles({ name: "uitvraag.txt", mimeType: "text/plain", buffer: Buffer.from("De leverancier moet persoonsgegevens versleutelen tijdens transport en opslag.") });
  await page.getByRole("button", { name: "Document uploaden", exact: true }).click();
  await expect(page.getByText("uitvraag.txt", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Eisen extraheren", exact: true }).click();
  await page.getByRole("link", { name: "Eisen", exact: true }).click();
  await expect(page.getByText(/persoonsgegevens versleutelen/).first()).toBeVisible();

  await page.getByRole("link", { name: "Bewijsbibliotheek", exact: true }).click();
  await page.getByLabel("Titel", { exact: true }).fill("Encryptiebeleid");
  await page.getByLabel("Bestand *", { exact: true }).setInputFiles({ name: "bewijs.txt", mimeType: "text/plain", buffer: Buffer.from("Alle gegevens zijn met AES-256 versleuteld en TLS 1.3 beschermt transport.") });
  await page.getByRole("button", { name: "Bewijsstuk toevoegen", exact: true }).click();
  await expect(page.getByText("Encryptiebeleid", { exact: true }).first()).toBeVisible();

  await page.getByRole("link", { name: "Eisen-bewijsmatrix", exact: true }).click();
  await page.getByRole("button", { name: "Bewijsvoorstellen genereren", exact: true }).click();
  await expect(page.getByText("Encryptiebeleid", { exact: true }).first()).toBeVisible();
  const row = page.locator("tbody tr").first();
  await row.getByText("Beoordelen", { exact: true }).click();
  await row.getByLabel("Beoordelingsstatus", { exact: true }).selectOption("voldoende onderbouwd");
  await row.getByRole("button", { name: "Menselijke beoordeling opslaan", exact: true }).click();
  await expect(row.getByText("voldoende onderbouwd", { exact: true }).first()).toBeVisible();

  await page.getByRole("link", { name: "Export", exact: true }).click();
  await expect(page.getByRole("link", { name: "CSV-matrix downloaden", exact: true })).toBeVisible();
});
