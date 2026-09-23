"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { resetDemo } from "@/lib/api/client";

export async function resetDemoAction() {
  await resetDemo();
  revalidatePath("/");
  revalidatePath("/dossiers");
  revalidatePath("/projecten/demo-waterdam");
  redirect("/projecten/demo-waterdam?tab=overzicht");
}
