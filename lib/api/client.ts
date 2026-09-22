import "server-only";

import type { components } from "@/lib/api/schema";

export type ProjectCreate = components["schemas"]["ProjectCreate"];
export type ProjectResponse = components["schemas"]["ProjectResponse"];
export type WorkspaceResponse = components["schemas"]["WorkspaceResponse"];
export type RequirementCreate = components["schemas"]["RequirementCreate"];
export type RequirementUpdate = components["schemas"]["RequirementUpdate"];
export type AssessmentUpsert = components["schemas"]["AssessmentUpsert"];

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
    const headers = new Headers(init?.headers);
    if (init?.body && !(init.body instanceof FormData) && !headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }
    response = await fetch(`${apiUrl()}${path}`, {
      ...init,
      cache: "no-store",
      headers,
      signal: AbortSignal.timeout(30_000),
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

async function requestResponse(path: string, init?: RequestInit): Promise<Response> {
  try {
    const response = await fetch(`${apiUrl()}${path}`, {
      ...init,
      cache: "no-store",
      signal: AbortSignal.timeout(30_000),
    });
    if (!response.ok) throw new PythonApiError("De export kon niet worden aangemaakt.", response.status);
    return response;
  } catch (error) {
    if (error instanceof PythonApiError) throw error;
    throw new PythonApiError("De Python-backend is niet bereikbaar.", 503);
  }
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

export function getWorkspace(projectId: string): Promise<WorkspaceResponse> {
  return request<WorkspaceResponse>(`/api/v1/projects/${encodeURIComponent(projectId)}/workspace`);
}

export function uploadSource(projectId: string, form: FormData) {
  return request(`/api/v1/projects/${encodeURIComponent(projectId)}/source-documents`, {
    method: "POST",
    body: form,
  });
}

export function extractRequirements(projectId: string, documentId: string) {
  return request(`/api/v1/projects/${encodeURIComponent(projectId)}/source-documents/${encodeURIComponent(documentId)}/extract`, { method: "POST" });
}

export function addRequirement(projectId: string, input: RequirementCreate) {
  return request(`/api/v1/projects/${encodeURIComponent(projectId)}/requirements`, {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function updateRequirement(projectId: string, requirementId: string, input: RequirementUpdate) {
  return request(`/api/v1/projects/${encodeURIComponent(projectId)}/requirements/${encodeURIComponent(requirementId)}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export function deleteRequirement(projectId: string, requirementId: string) {
  return request(`/api/v1/projects/${encodeURIComponent(projectId)}/requirements/${encodeURIComponent(requirementId)}`, { method: "DELETE" });
}

export function mergeRequirements(projectId: string, primaryId: string, secondaryId: string) {
  return request(`/api/v1/projects/${encodeURIComponent(projectId)}/requirements/merge`, {
    method: "POST",
    body: JSON.stringify({ primaryId, secondaryId }),
  });
}

export function uploadEvidence(projectId: string, form: FormData) {
  return request(`/api/v1/projects/${encodeURIComponent(projectId)}/evidence-documents`, {
    method: "POST",
    body: form,
  });
}

export function generateMatches(projectId: string) {
  return request(`/api/v1/projects/${encodeURIComponent(projectId)}/matches/generate`, { method: "POST" });
}

export function saveAssessment(projectId: string, requirementId: string, input: AssessmentUpsert) {
  return request(`/api/v1/projects/${encodeURIComponent(projectId)}/requirements/${encodeURIComponent(requirementId)}/assessment`, {
    method: "PUT",
    body: JSON.stringify(input),
  });
}

export function getCsvExport(projectId: string): Promise<Response> {
  return requestResponse(`/api/v1/projects/${encodeURIComponent(projectId)}/export.csv`);
}

export function getEvidenceFile(projectId: string, documentId: string): Promise<Response> {
  return requestResponse(`/api/v1/projects/${encodeURIComponent(projectId)}/evidence-documents/${encodeURIComponent(documentId)}/file`);
}
