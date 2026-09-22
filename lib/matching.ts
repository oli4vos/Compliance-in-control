import type { EvidenceDocument, Project, Requirement } from "@prisma/client";

export type MatchProposal = { evidenceDocumentId: string; fragment: string; sourceLocation: string; score: number; explanation: string; warnings: string };
export interface EvidenceMatcher { match(requirement: Requirement, evidence: EvidenceDocument[], project: Project): MatchProposal[] | Promise<MatchProposal[]> }

const stop = new Set(["de", "het", "een", "en", "van", "voor", "dat", "met", "moet", "dient", "worden", "zijn", "aan", "op", "in", "te"]);
export function tokens(text: string) { return [...new Set(text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").match(/[a-z0-9-]{3,}/g) ?? [])].filter(x => !stop.has(x)); }

export class LocalEvidenceMatcher implements EvidenceMatcher {
  match(requirement: Requirement, evidence: EvidenceDocument[], project: Project) {
    const req = tokens(`${requirement.title} ${requirement.originalText} ${requirement.category}`);
    return evidence.map(doc => {
      const docTokens = new Set(tokens(`${doc.title} ${doc.description} ${doc.tags} ${doc.extractedText}`));
      const shared = req.filter(token => docTokens.has(token));
      const categoryBoost = categoryTerms(requirement.category).some(t => docTokens.has(t)) ? 18 : 0;
      const score = Math.min(96, Math.round((shared.length / Math.max(req.length, 1)) * 100 + categoryBoost));
      const sentences = doc.extractedText.split(/(?<=[.!?])\s+|\n+/).filter(Boolean);
      const fragment = sentences.sort((a, b) => overlap(b, req) - overlap(a, req))[0]?.slice(0, 700) ?? "";
      const warnings: string[] = [];
      if (doc.product && doc.product.toLowerCase() !== project.product.toLowerCase()) warnings.push(`Productscope wijkt af (${doc.product}).`);
      if (doc.productVersion && doc.productVersion !== project.productVersion) warnings.push(`Versie ${doc.productVersion} wijkt af van ${project.productVersion}.`);
      if (doc.organization && doc.organization.toLowerCase() !== "planwijzer systemen b.v.") warnings.push(`Controleer juridische entiteit: ${doc.organization}.`);
      if (doc.expiresAt && doc.expiresAt < new Date()) warnings.push("Bewijsstuk is verlopen.");
      if (!fragment) warnings.push("Geen letterlijk bronfragment gevonden; zwak voorstel.");
      return { evidenceDocumentId: doc.id, fragment, sourceLocation: "Geëxtraheerde tekst", score, explanation: shared.length ? `Overlap op: ${shared.slice(0, 5).join(", ")}.` : "Beperkte inhoudelijke overlap; handmatige controle nodig.", warnings: warnings.join(" ") };
    }).filter(m => m.score >= 10).sort((a, b) => b.score - a.score).slice(0, 5);
  }
}

export class OpenAIEvidenceMatcher implements EvidenceMatcher {
  constructor(private apiKey:string,private fallback=new LocalEvidenceMatcher()){}
  async match(requirement:Requirement,evidence:EvidenceDocument[],project:Project){
    try{
      const docs=evidence.map(e=>({id:e.id,title:e.title,organization:e.organization,product:e.product,version:e.productVersion,environment:e.environment,expiresAt:e.expiresAt?.toISOString(),text:e.extractedText.slice(0,9000)}));
      const response=await fetch("https://api.openai.com/v1/responses",{method:"POST",headers:{"Authorization":`Bearer ${this.apiKey}`,"Content-Type":"application/json"},body:JSON.stringify({model:process.env.OPENAI_MODEL||"gpt-6-astra",store:false,instructions:"Beoordeel welke bewijsstukken mogelijk relevant zijn voor de eis. Geef voorstellen, nooit een definitief complianceoordeel. fragment moet een letterlijk fragment uit het bewijs zijn. Score 0-100. Benoem scope-, versie-, entiteits-, omgevings- en geldigheidsrisico's.",input:JSON.stringify({requirement:{text:requirement.originalText,category:requirement.category},project:{product:project.product,version:project.productVersion},evidence:docs}),text:{format:{type:"json_schema",name:"matches",strict:true,schema:{type:"object",additionalProperties:false,properties:{matches:{type:"array",items:{type:"object",additionalProperties:false,properties:{evidenceDocumentId:{type:"string"},fragment:{type:"string"},sourceLocation:{type:"string"},score:{type:"integer"},explanation:{type:"string"},warnings:{type:"string"}},required:["evidenceDocumentId","fragment","sourceLocation","score","explanation","warnings"]}}},required:["matches"]}}}})});
      if(!response.ok)throw new Error("LLM-matching niet beschikbaar");const json=await response.json() as {output?:Array<{content?:Array<{type:string;text?:string}>}>};const output=json.output?.flatMap(o=>o.content??[]).find(c=>c.type==="output_text")?.text;const parsed=JSON.parse(output||"{}") as {matches?:MatchProposal[]};
      return (parsed.matches??[]).filter(m=>evidence.some(e=>e.id===m.evidenceDocumentId)).map(m=>{const doc=evidence.find(e=>e.id===m.evidenceDocumentId)!;const literal=doc.extractedText.includes(m.fragment);return {...m,score:Math.max(0,Math.min(100,Math.round(m.score))),fragment:literal?m.fragment:"",warnings:literal?m.warnings:`${m.warnings} Geen verifieerbaar letterlijk fragment; zwak voorstel.`.trim()}});
    }catch{return this.fallback.match(requirement,evidence,project)}
  }
}
export function evidenceMatcher(){return process.env.OPENAI_API_KEY?new OpenAIEvidenceMatcher(process.env.OPENAI_API_KEY):new LocalEvidenceMatcher()}
function overlap(text: string, req: string[]) { const t = new Set(tokens(text)); return req.filter(x => t.has(x)).length; }
function categoryTerms(category: string) { return tokens({ "informatiebeveiliging": "beveiliging encryptie logging toegang audit", privacy: "privacy persoonsgegevens bewaartermijn subverwerker eer", "AI en algoritmen": "algoritme model ai menselijk uitleg", continuïteit: "continuïteit herstel beschikbaarheid" }[category] ?? category); }

export function expiryState(expiresAt: Date | null, now = new Date()) {
  if (!expiresAt) return "geldig";
  if (expiresAt < now) return "verlopen";
  if (expiresAt.getTime() - now.getTime() <= 30 * 86400000) return "verloopt binnenkort";
  return "geldig";
}
