import { test, expect } from "@playwright/test";

test("projecten worden via de Python-backend aangemaakt en getoond", async ({ page, request }) => {
  const name = `Python dossier ${Date.now()}`;

  await page.goto("/projecten/nieuw");
  await page.getByLabel("Projectnaam *", { exact: true }).fill(name);
  await page.getByLabel("Opdrachtgever *", { exact: true }).fill("Fictieve Organisatie B.V.");
  await page.getByLabel("Aanbestedingsnummer of referentie", { exact: true }).fill("PY-001");
  await page.getByRole("button", { name: "Dossier aanmaken", exact: true }).click();
  await expect(page.getByRole("heading", { name, exact: true })).toBeVisible();

  const apiResponse = await request.get("http://127.0.0.1:8000/api/v1/projects");
  expect(apiResponse.ok()).toBeTruthy();
  const projects = await apiResponse.json() as Array<{ name: string }>;
  expect(projects.some((project) => project.name === name)).toBeTruthy();

  await page.goto("/");
  await expect(page.getByRole("heading", { name, exact: true })).toBeVisible();
});
