import "server-only";

import type { components } from "@/lib/api/schema";

export type ProjectCreate = components["schemas"]["ProjectCreate"];
export type ProjectResponse = components["schemas"]["ProjectResponse"];

const apiUrl = () => (process.env.PYTHON_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

export class PythonApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "PythonApiError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${apiUrl()}${path}`, {
      ...init,
      cache: "no-store",
      headers: { "Content-Type": "application/json", ...init?.headers },
      signal: AbortSignal.timeout(8_000),
    });
  } catch {
    throw new PythonApiError(
      "De Python-backend is niet bereikbaar. Start de volledige omgeving met npm run dev:stack.",
      503,
    );
  }

  if (!response.ok) {
    let message = "De Python-backend kon het verzoek niet verwerken.";
    try {
      const body = (await response.json()) as { detail?: string | Array<{ msg?: string }> };
      if (typeof body.detail === "string") message = body.detail;
      else if (Array.isArray(body.detail)) message = body.detail.map((item) => item.msg).filter(Boolean).join(" ") || message;
    } catch {
      // De veilige generieke melding blijft staan als de API geen JSON retourneert.
    }
    throw new PythonApiError(message, response.status);
  }

  return response.json() as Promise<T>;
}

export function listProjects(): Promise<ProjectResponse[]> {
  return request<ProjectResponse[]>("/api/v1/projects");
}

export function getProject(projectId: string): Promise<ProjectResponse> {
  return request<ProjectResponse>(`/api/v1/projects/${encodeURIComponent(projectId)}`);
}

export function createProject(
  input: ProjectCreate,
  idempotencyKey: string,
): Promise<ProjectResponse> {
  return request<ProjectResponse>("/api/v1/projects", {
    method: "POST",
    headers: { "Idempotency-Key": idempotencyKey },
    body: JSON.stringify(input),
  });
}
