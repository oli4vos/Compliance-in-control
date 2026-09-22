import { getEvidenceFile } from "@/lib/api/client";

export async function GET(
  _: Request,
  { params }: { params: Promise<{ id: string; docId: string }> },
) {
  const { id, docId } = await params;
  try {
    const response = await getEvidenceFile(id, docId);
    return new Response(await response.arrayBuffer(), {
      headers: {
        "Content-Type": response.headers.get("Content-Type") || "application/octet-stream",
        "Content-Disposition": response.headers.get("Content-Disposition") || "attachment",
      },
    });
  } catch {
    return new Response("Bestand niet gevonden", { status: 404 });
  }
}
