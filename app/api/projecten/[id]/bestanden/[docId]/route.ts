import { readFile } from "node:fs/promises";
import path from "node:path";
import { db } from "@/lib/db";
export async function GET(_:Request,{params}:{params:Promise<{id:string;docId:string}>}){const {id,docId}=await params;const doc=await db.evidenceDocument.findFirst({where:{id:docId,projectId:id}});if(!doc)return new Response("Bestand niet gevonden",{status:404});const safeProject=id.replace(/[^a-zA-Z0-9_-]/g,"");const safeFile=path.basename(doc.storedName);if(safeProject!==id||safeFile!==doc.storedName)return new Response("Ongeldige bestandsreferentie",{status:400});try{const data=await readFile(path.join(process.cwd(),"storage","uploads",safeProject,safeFile));return new Response(data,{headers:{"Content-Type":doc.mimeType,"Content-Disposition":`attachment; filename="${doc.fileName.replace(/[\r\n"]/g,"_")}"`}})}catch{return new Response("Bestand is niet lokaal aanwezig",{status:404})}}

