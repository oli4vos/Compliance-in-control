import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./e2e",
  workers: 1,
  use: { baseURL: "http://127.0.0.1:3000", trace: "on-first-retry" },
  webServer: [
    { command: "bash scripts/start-api-e2e.sh", url: "http://127.0.0.1:8000/health", reuseExistingServer: true, timeout: 120000 },
    { command: "npm run dev", url: "http://127.0.0.1:3000", reuseExistingServer: true, timeout: 120000, env: { PYTHON_API_URL: "http://127.0.0.1:8000" } },
  ],
});
