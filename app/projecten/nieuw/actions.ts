"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { createProject } from "@/lib/api/client";
import { db } from "@/lib/db";

function value(form: FormData, key: string) {
  return String(form.get(key) ?? "").trim();
}

function legacyDate(raw: string) {
  return raw ? new Date(`${raw}T12:00:00`) : null;
}

export async function createPythonProjectAction(form: FormData) {
  const name = value(form, "name");
  const client = value(form, "client");
  if (!name || !client) throw new Error("Projectnaam en opdrachtgever zijn verplicht.");

  const dueDate = value(form, "dueDate");
  const project = await createProject(
    {
      name,
      client,
      reference: value(form, "reference"),
      dueDate: dueDate || null,
      product: value(form, "product"),
      productVersion: value(form, "productVersion"),
      owner: value(form, "owner"),
      notes: value(form, "notes"),
    },
    value(form, "idempotencyKey"),
  );

  // Tijdelijke read/write-projectie voor de nog niet gemigreerde document- en matrixmodules.
  // Python blijft de bron van waarheid; deze projectie verdwijnt na de documentmigratie.
  await db.project.upsert({
    where: { id: project.id },
    update: {
      name: project.name,
      client: project.client,
      reference: project.reference,
      dueDate: legacyDate(project.dueDate || ""),
      product: project.product,
      productVersion: project.productVersion,
      owner: project.owner,
      notes: project.notes,
    },
    create: {
      id: project.id,
      name: project.name,
      client: project.client,
      reference: project.reference,
      dueDate: legacyDate(project.dueDate || ""),
      product: project.product,
      productVersion: project.productVersion,
      owner: project.owner,
      notes: project.notes,
      auditEvents: {
        create: {
          action: "Python-project geprojecteerd",
          entity: `Project:${project.id}`,
          newValue: project.name,
          user: "Systeem",
        },
      },
    },
  });

  revalidatePath("/");
  redirect(`/projecten/${project.id}`);
}
