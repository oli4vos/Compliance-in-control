import { db } from "@/lib/db";
import { DISCLAIMER } from "@/lib/constants";
function csv(v:unknown){return `"${String(v??"").replaceAll('"','""')}"`}
export async function GET(_:Request,{params}:{params:Promise<{id:string}>}){
  const {id}=await params;
  const p=await db.project.findUnique({
    where:{id},
    include:{requirements:{orderBy:{number:"asc"},include:{sourceDocument:true,matches:{orderBy:{score:"desc"},include:{evidenceDocument:true}},assessments:{orderBy:{updatedAt:"desc"}}}}}
  });
  if(!p)return new Response("Dossier niet gevonden",{status:404});
  const head=["Nummer","Titel","Categorie","Verplicht/wens","Bronbestand","Bronlocatie","Oorspronkelijke eis","Bronfragment","Menselijke status","Gekoppeld bewijs","Bewijsfragment","Matchscore","Waarschuwingen","Conceptantwoord","Opmerkingen","Eigenaar","Beoordelingsdatum"];
  const rows=p.requirements.map(r=>{const a=r.assessments[0],m=(a?.evidenceMatchId?r.matches.find(x=>x.id===a.evidenceMatchId):r.matches[0]);return [r.number,r.title,r.category,r.priority,r.sourceDocument?.name||"Handmatig",r.sourceLocation,r.originalText,r.sourceFragment,r.status,m?.evidenceDocument.title||"",m?.fragment||"",m?.score??"",m?.warnings||"",a?.draftAnswer||"",a?.notes||"",a?.owner||"",a?.assessedAt.toISOString()||""]});
  const out=[["DISCLAIMER",DISCLAIMER],[],head,...rows].map(row=>row.map(csv).join(";")).join("\r\n");
  return new Response("\uFEFF"+out,{headers:{"Content-Type":"text/csv; charset=utf-8","Content-Disposition":`attachment; filename="${p.reference||"dossier"}-eisen-bewijsmatrix.csv"`}});
}
