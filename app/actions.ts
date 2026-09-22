"use server";

import { randomUUID } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { db } from "@/lib/db";
import { extractText, requirementExtractor, paragraphs, shortTitle, categorize } from "@/lib/extraction";
import { evidenceMatcher } from "@/lib/matching";

const MAX_SIZE = 10 * 1024 * 1024;
const allowed = new Set(["pdf", "docx", "txt"]);
const user = "Lokale gebruiker";

function value(form: FormData, key: string) { return String(form.get(key) ?? "").trim(); }
function dateValue(raw: string) { return raw ? new Date(`${raw}T12:00:00`) : null; }

export async function createProjectAction(form: FormData) {
  const name = value(form, "name");
  const client = value(form, "client");
  if (!name || !client) throw new Error("Projectnaam en opdrachtgever zijn verplicht.");
  const project = await db.project.create({ data: {
    name, client, reference: value(form, "reference"), dueDate: dateValue(value(form, "dueDate")), product: value(form, "product"), productVersion: value(form, "productVersion"), owner: value(form, "owner"), notes: value(form, "notes"),
    auditEvents: { create: { action: "Dossier aangemaakt", entity: "Project", newValue: name, user } },
  }});
  redirect(`/projecten/${project.id}`);
}

async function saveUpload(projectId: string, file: File) {
  if (!file || file.size === 0) throw new Error("Kies een bestand.");
  if (file.size > MAX_SIZE) throw new Error("Het bestand is groter dan 10 MB.");
  const original = path.basename(file.name).replace(/[^a-zA-Z0-9._ -]/g, "_");
  const ext = original.toLowerCase().split(".").pop() ?? "";
  if (!allowed.has(ext)) throw new Error("Alleen PDF-, DOCX- en TXT-bestanden zijn toegestaan.");
  const safeProject = projectId.replace(/[^a-zA-Z0-9_-]/g, "");
  if (safeProject !== projectId) throw new Error("Ongeldige projectreferentie.");
  const storedName = `${randomUUID()}.${ext}`;
  const dir = path.join(process.cwd(), "storage", "uploads", safeProject);
  await mkdir(dir, { recursive: true });
  await writeFile(path.join(dir, storedName), Buffer.from(await file.arrayBuffer()), { flag: "wx" });
  const extracted = await extractText(file);
  return { original, storedName, mimeType: file.type || "application/octet-stream", ...extracted };
}

export async function uploadSourceAction(projectId: string, form: FormData) {
  const project = await db.project.findUnique({ where: { id: projectId } });
  if (!project) throw new Error("Dossier niet gevonden.");
  const upload = await saveUpload(projectId, form.get("file") as File);
  const doc = await db.sourceDocument.create({ data: { projectId, name: upload.original, storedName: upload.storedName, type: value(form, "type"), mimeType: upload.mimeType, extractedText: upload.text } });
  await db.auditEvent.create({ data: { projectId, action: "Brondocument toegevoegd", entity: `SourceDocument:${doc.id}`, newValue: doc.name, user } });
  revalidatePath(`/projecten/${projectId}`);
}

export async function extractRequirementsAction(projectId: string, documentId: string) {
  const doc = await db.sourceDocument.findFirst({ where: { id: documentId, projectId } });
  if (!doc) throw new Error("Brondocument niet gevonden.");
  const extractor = requirementExtractor();
  const candidates = await extractor.extract(paragraphs(doc.extractedText));
  const count = await db.requirement.count({ where: { projectId } });
  for (let i = 0; i < candidates.length; i++) {
    const item = candidates[i];
    const number = `E-${String(count + i + 1).padStart(3, "0")}`;
    await db.requirement.upsert({ where: { projectId_number: { projectId, number } }, update: {}, create: { projectId, sourceDocumentId: doc.id, number, title: item.title, originalText: item.text, category: item.category, sourceLocation: item.location, sourceFragment: item.fragment, priority: item.priority, origin: "automatisch" } });
  }
  await db.auditEvent.create({ data: { projectId, action: "Eisen geëxtraheerd", entity: `SourceDocument:${doc.id}`, newValue: `${candidates.length} concept-eisen`, user } });
  revalidatePath(`/projecten/${projectId}`);
}

export async function addRequirementAction(projectId: string, form: FormData) {
  const text = value(form, "originalText");
  if (!text) throw new Error("De tekst van de eis is verplicht.");
  const count = await db.requirement.count({ where: { projectId } });
  const req = await db.requirement.create({ data: { projectId, number: `E-${String(count + 1).padStart(3, "0")}`, title: value(form, "title") || shortTitle(text), originalText: text, category: value(form, "category") || categorize(text), sourceLocation: "Handmatig toegevoegd", sourceFragment: text, priority: value(form, "priority") || "verplicht", origin: "handmatig" } });
  await db.auditEvent.create({ data: { projectId, requirementId: req.id, action: "Eis toegevoegd", entity: `Requirement:${req.id}`, newValue: text, user } });
  revalidatePath(`/projecten/${projectId}`);
}

export async function updateRequirementAction(projectId: string, requirementId: string, form: FormData) {
  const existing = await db.requirement.findFirst({ where: { id: requirementId, projectId } });
  if (!existing) throw new Error("Eis niet gevonden.");
  const data = { title: value(form, "title"), originalText: value(form, "originalText"), category: value(form, "category"), priority: value(form, "priority"), notApplicable: form.get("notApplicable") === "on" };
  await db.requirement.update({ where: { id: requirementId }, data: { ...data, status: data.notApplicable ? "niet van toepassing" : existing.status } });
  await db.auditEvent.create({ data: { projectId, requirementId, action: "Eis bijgewerkt", entity: `Requirement:${requirementId}`, oldValue: JSON.stringify({ title: existing.title, category: existing.category }), newValue: JSON.stringify(data), user } });
  revalidatePath(`/projecten/${projectId}`);
}

export async function deleteRequirementAction(projectId: string, requirementId: string) {
  const req = await db.requirement.findFirst({ where: { id: requirementId, projectId } });
  if (!req) return;
  await db.$transaction([
    db.auditEvent.create({ data: { projectId, action: "Eis verwijderd", entity: `Requirement:${requirementId}`, oldValue: req.originalText, user } }),
    db.requirement.delete({ where: { id: requirementId } }),
  ]);
  revalidatePath(`/projecten/${projectId}`);
}

export async function mergeRequirementsAction(projectId: string, form: FormData) {
  const primaryId = value(form, "primaryId"), secondaryId = value(form, "secondaryId");
  if (!primaryId || !secondaryId || primaryId === secondaryId) throw new Error("Kies twee verschillende eisen.");
  const [a, b] = await Promise.all([db.requirement.findFirst({ where: { id: primaryId, projectId } }), db.requirement.findFirst({ where: { id: secondaryId, projectId } })]);
  if (!a || !b) throw new Error("Een van de eisen bestaat niet.");
  await db.requirement.update({ where: { id: a.id }, data: { originalText: `${a.originalText}\n\nSamengevoegd met ${b.number}: ${b.originalText}`, sourceFragment: `${a.sourceFragment}\n---\n${b.sourceFragment}`, title: `${a.title} / ${b.title}`.slice(0, 120) } });
  await db.requirement.delete({ where: { id: b.id } });
  await db.auditEvent.create({ data: { projectId, requirementId: a.id, action: "Eisen samengevoegd", entity: `Requirement:${a.id}`, oldValue: b.number, newValue: a.number, user } });
  revalidatePath(`/projecten/${projectId}`);
}

export async function uploadEvidenceAction(projectId: string, form: FormData) {
  const project = await db.project.findUnique({ where: { id: projectId } });
  if (!project) throw new Error("Dossier niet gevonden.");
  const upload = await saveUpload(projectId, form.get("file") as File);
  const doc = await db.evidenceDocument.create({ data: { projectId, title: value(form, "title") || upload.original, documentType: value(form, "documentType"), description: value(form, "description"), organization: value(form, "organization"), product: value(form, "product"), productVersion: value(form, "productVersion"), environment: value(form, "environment"), owner: value(form, "owner"), issuedAt: dateValue(value(form, "issuedAt")), expiresAt: dateValue(value(form, "expiresAt")), confidentiality: value(form, "confidentiality"), tags: value(form, "tags"), fileName: upload.original, storedName: upload.storedName, mimeType: upload.mimeType, extractedText: upload.text } });
  await db.auditEvent.create({ data: { projectId, action: "Bewijsstuk toegevoegd", entity: `EvidenceDocument:${doc.id}`, newValue: doc.title, user } });
  revalidatePath(`/projecten/${projectId}`);
}

export async function generateMatchesAction(projectId: string) {
  const project = await db.project.findUnique({ where: { id: projectId }, include: { requirements: true, evidenceDocuments: true } });
  if (!project) throw new Error("Dossier niet gevonden.");
  const matcher = evidenceMatcher();
  for (const requirement of project.requirements) {
    for (const proposal of await matcher.match(requirement, project.evidenceDocuments, project)) {
      await db.evidenceMatch.upsert({ where: { requirementId_evidenceDocumentId: { requirementId: requirement.id, evidenceDocumentId: proposal.evidenceDocumentId } }, update: proposal, create: { requirementId: requirement.id, ...proposal } });
    }
  }
  await db.auditEvent.create({ data: { projectId, action: "Bewijsvoorstellen gegenereerd", entity: "Project", newValue: "Lokale matcher", user } });
  revalidatePath(`/projecten/${projectId}`);
}

export async function saveAssessmentAction(projectId: string, requirementId: string, form: FormData) {
  const req = await db.requirement.findFirst({ where: { id: requirementId, projectId }, include: { assessments: true } });
  if (!req) throw new Error("Eis niet gevonden.");
  const status = value(form, "status");
  const data = { status, draftAnswer: value(form, "draftAnswer"), notes: value(form, "notes"), owner: value(form, "owner"), deadline: dateValue(value(form, "deadline")), approved: form.get("approved") === "on", assessedBy: user, evidenceMatchId: value(form, "evidenceMatchId") || null };
  const current = req.assessments[0];
  if (current) await db.assessment.update({ where: { id: current.id }, data }); else await db.assessment.create({ data: { requirementId, ...data } });
  await db.requirement.update({ where: { id: requirementId }, data: { status } });
  await db.auditEvent.create({ data: { projectId, requirementId, action: "Menselijke beoordeling vastgelegd", entity: `Requirement:${requirementId}`, oldValue: req.status, newValue: status, user } });
  if (data.deadline) await db.task.upsert({ where: { id: (await db.task.findFirst({ where: { requirementId } }))?.id ?? "new" }, update: { owner: data.owner, deadline: data.deadline, status: status === "voldoende onderbouwd" ? "afgerond" : "open" }, create: { projectId, requirementId, title: `Beoordeling afronden voor ${req.number}`, owner: data.owner, deadline: data.deadline } });
  revalidatePath(`/projecten/${projectId}`);
}
