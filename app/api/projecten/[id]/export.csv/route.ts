import { getCsvExport } from "@/lib/api/client";

export async function GET(_: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  try {
    const response = await getCsvExport(id);
    return new Response(await response.arrayBuffer(), {
      headers: {
        "Content-Type": response.headers.get("Content-Type") || "text/csv; charset=utf-8",
        "Content-Disposition": response.headers.get("Content-Disposition") || "attachment",
      },
    });
  } catch {
    return new Response("Dossier niet gevonden", { status: 404 });
  }
}
