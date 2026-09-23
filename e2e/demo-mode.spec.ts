import { test, expect } from "@playwright/test";

test("demo-modus toont identiteit en kan terugzetten", async ({ page }) => {
  await page.goto("/demo");
  await expect(page.getByRole("heading", { name: "Stap in als dossierbeheerder." })).toBeVisible();
  await expect(page.getByText("Eva de Vries", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Demo terugzetten naar beginsituatie" }).click();
  await expect(page.getByRole("heading", { name: "AI-planningssoftware Gemeente Waterdam" })).toBeVisible();

  await page.goto("/demo");
  await page.getByRole("link", { name: "Open eisen-bewijsmatrix" }).click();
  await expect(page.getByRole("heading", { name: "AI-planningssoftware Gemeente Waterdam" })).toBeVisible();

  await page.goto("/demo");
  await page.getByRole("button", { name: "Demo terugzetten naar beginsituatie" }).click();
  await expect(page.getByRole("heading", { name: "AI-planningssoftware Gemeente Waterdam" })).toBeVisible();
});
