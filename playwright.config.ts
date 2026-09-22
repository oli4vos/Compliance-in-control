import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./e2e",
  workers: 1,
  use: { baseURL: "http://127.0.0.1:3100", trace: "on-first-retry" },
  webServer: [
    { command: "bash scripts/start-api-e2e.sh", url: "http://127.0.0.1:18000/health", reuseExistingServer: false, timeout: 120000 },
    { command: "npm run dev -- --hostname 127.0.0.1 --port 3100", url: "http://127.0.0.1:3100", reuseExistingServer: false, timeout: 120000, env: { PYTHON_API_URL: "http://127.0.0.1:18000" } },
  ],
});
