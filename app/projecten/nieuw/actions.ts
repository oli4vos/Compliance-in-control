"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { createProject } from "@/lib/api/client";

function value(form: FormData, key: string) {
  return String(form.get(key) ?? "").trim();
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

  revalidatePath("/");
  redirect(`/projecten/${project.id}`);
}
