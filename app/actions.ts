"use server";

import { revalidatePath } from "next/cache";
import {
  addRequirement,
  deleteRequirement,
  extractRequirements,
  generateMatches,
  mergeRequirements,
  saveAssessment,
  updateRequirement,
  uploadEvidence,
  uploadSource,
} from "@/lib/api/client";

function value(form: FormData, key: string) {
  return String(form.get(key) ?? "").trim();
}

function refresh(projectId: string) {
  revalidatePath("/");
  revalidatePath(`/projecten/${projectId}`);
  revalidatePath(`/projecten/${projectId}/dossier`);
}

export async function uploadSourceAction(projectId: string, form: FormData) {
  await uploadSource(projectId, form);
  refresh(projectId);
}

export async function extractRequirementsAction(projectId: string, documentId: string) {
  await extractRequirements(projectId, documentId);
  refresh(projectId);
}

export async function addRequirementAction(projectId: string, form: FormData) {
  const originalText = value(form, "originalText");
  if (!originalText) throw new Error("De tekst van de eis is verplicht.");
  await addRequirement(projectId, {
    title: value(form, "title"),
    originalText,
    category: value(form, "category") || "overig",
    priority: value(form, "priority") || "verplicht",
  });
  refresh(projectId);
}

export async function updateRequirementAction(
  projectId: string,
  requirementId: string,
  form: FormData,
) {
  await updateRequirement(projectId, requirementId, {
    title: value(form, "title"),
    originalText: value(form, "originalText"),
    category: value(form, "category"),
    priority: value(form, "priority"),
    notApplicable: form.get("notApplicable") === "on",
  });
  refresh(projectId);
}

export async function deleteRequirementAction(projectId: string, requirementId: string) {
  await deleteRequirement(projectId, requirementId);
  refresh(projectId);
}

export async function mergeRequirementsAction(projectId: string, form: FormData) {
  const primaryId = value(form, "primaryId");
  const secondaryId = value(form, "secondaryId");
  if (!primaryId || !secondaryId || primaryId === secondaryId) {
    throw new Error("Kies twee verschillende eisen.");
  }
  await mergeRequirements(projectId, primaryId, secondaryId);
  refresh(projectId);
}

export async function uploadEvidenceAction(projectId: string, form: FormData) {
  await uploadEvidence(projectId, form);
  refresh(projectId);
}

export async function generateMatchesAction(projectId: string) {
  await generateMatches(projectId);
  refresh(projectId);
}

export async function saveAssessmentAction(
  projectId: string,
  requirementId: string,
  form: FormData,
) {
  const deadline = value(form, "deadline");
  await saveAssessment(projectId, requirementId, {
    status: value(form, "status"),
    draftAnswer: value(form, "draftAnswer"),
    notes: value(form, "notes"),
    owner: value(form, "owner"),
    deadline: deadline || null,
    approved: form.get("approved") === "on",
    evidenceMatchId: value(form, "evidenceMatchId") || null,
  });
  refresh(projectId);
}
