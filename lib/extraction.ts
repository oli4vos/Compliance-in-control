import mammoth from "mammoth";

export type ExtractedFragment = { text: string; location: string };
export interface RequirementCandidate { text: string; title: string; category: string; location: string; fragment: string; priority: string }
export interface RequirementExtractor { extract(fragments: ExtractedFragment[]): RequirementCandidate[] | Promise<RequirementCandidate[]> }

const signals = ["moet", "dient", "verplicht", "vereist", "inschrijver toont aan", "opdrachtnemer waarborgt", "leverancier beschrijft", "bewijsstuk", "certificaat", "beveiliging", "persoonsgegevens", "algoritme", "ai-systeem", "continuïteit", "subverwerker"];

export function categorize(text: string) {
  const t = text.toLowerCase();
  if (/encrypt|versleutel|toegang|logging|beveilig|pentest/.test(t)) return "informatiebeveiliging";
  if (/persoonsgegeven|bewaartermijn|subverwerk|\beer\b|privacy/.test(t)) return "privacy";
  if (/algorit|ai-systeem|model|menselijke tussenkomst|uitleg/.test(t)) return "AI en algoritmen";
  if (/continuïteit|herstel|beschikbaarheid/.test(t)) return "continuïteit";
  if (/governance|organisatie|verantwoordelijk/.test(t)) return "organisatie en governance";
  if (/contract|aansprak|voorwaarde/.test(t)) return "juridische voorwaarden";
  if (/duurzaam|milieu|energie/.test(t)) return "duurzaamheid";
  if (/financ|omzet|verzekering/.test(t)) return "financieel";
  return "overig";
}

export class LocalRequirementExtractor implements RequirementExtractor {
  extract(fragments: ExtractedFragment[]) {
    const found: RequirementCandidate[] = [];
    for (const fragment of fragments) {
      const lines = fragment.text.split(/(?<=[.!?])\s+|\n+/).map(s => s.trim()).filter(s => s.length > 20);
      for (const line of lines) {
        const lower = line.toLowerCase();
        if (!signals.some(signal => lower.includes(signal))) continue;
        const clean = line.replace(/^[-•\d.)\s]+/, "").trim();
        found.push({ text: clean, title: shortTitle(clean), category: categorize(clean), location: fragment.location, fragment: clean, priority: /wens|bij voorkeur/.test(lower) ? "wens" : "verplicht" });
      }
    }
    return found.filter((item, index, all) => all.findIndex(other => other.text.toLowerCase() === item.text.toLowerCase()) === index).slice(0, 80);
  }
}

export class OpenAIRequirementExtractor implements RequirementExtractor {
  constructor(private apiKey: string, private fallback = new LocalRequirementExtractor()) {}
  async extract(fragments: ExtractedFragment[]) {
    try {
      const input = fragments.map(f => `[${f.location}] ${f.text}`).join("\n").slice(0, 45000);
      const response = await fetch("https://api.openai.com/v1/responses", { method:"POST", headers:{"Authorization":`Bearer ${this.apiKey}`,"Content-Type":"application/json"}, body:JSON.stringify({ model:process.env.OPENAI_MODEL||"gpt-6-astra", store:false, instructions:"Extraheer uitsluitend expliciete eisen uit de Nederlandse aanbestedingstekst. Geef compacte JSON met een requirements-array. Bewaar de letterlijke eistekst en locatie. Een eis is nooit een juridisch oordeel.", input, text:{format:{type:"json_schema",name:"requirements",strict:true,schema:{type:"object",additionalProperties:false,properties:{requirements:{type:"array",items:{type:"object",additionalProperties:false,properties:{text:{type:"string"},title:{type:"string"},category:{type:"string"},location:{type:"string"},fragment:{type:"string"},priority:{type:"string"}},required:["text","title","category","location","fragment","priority"]}}},required:["requirements"]}}} }) });
      if (!response.ok) throw new Error("LLM-extractie niet beschikbaar");
      const json = await response.json() as { output?: Array<{content?:Array<{type:string;text?:string}>}> };
      const text = json.output?.flatMap(o=>o.content??[]).find(c=>c.type==="output_text")?.text;
      const parsed = JSON.parse(text||"{}") as {requirements?:RequirementCandidate[]};
      return (parsed.requirements??[]).map(r=>({...r,category:CATEGORIES_SET.has(r.category)?r.category:categorize(r.text),priority:r.priority==="wens"?"wens":"verplicht"}));
    } catch { return this.fallback.extract(fragments); }
  }
}
const CATEGORIES_SET=new Set(["informatiebeveiliging","privacy","AI en algoritmen","continuïteit","organisatie en governance","juridische voorwaarden","duurzaamheid","financieel","overig"]);

export function requirementExtractor(){ return process.env.OPENAI_API_KEY ? new OpenAIRequirementExtractor(process.env.OPENAI_API_KEY) : new LocalRequirementExtractor(); }

export function shortTitle(text: string) {
  const words = text.replace(/[.:;]$/, "").split(/\s+/).slice(0, 8).join(" ");
  return words.length > 62 ? words.slice(0, 59) + "…" : words;
}

export async function extractText(file: File): Promise<{ text: string; fragments: ExtractedFragment[] }> {
  const ext = file.name.toLowerCase().split(".").pop();
  const buffer = Buffer.from(await file.arrayBuffer());
  if (ext === "txt") {
    const text = buffer.toString("utf8").replace(/\0/g, "");
    return { text, fragments: paragraphs(text) };
  }
  if (ext === "docx") {
    const result = await mammoth.extractRawText({ buffer });
    return { text: result.value, fragments: paragraphs(result.value) };
  }
  if (ext === "pdf") {
    const { PDFParse } = await import("pdf-parse");
    const parser = new PDFParse({ data: new Uint8Array(buffer) });
    const result = await parser.getText();
    await parser.destroy();
    const pages = result.pages?.map((p: { text: string }, i: number) => ({ text: p.text, location: `Pagina ${i + 1}` })) ?? paragraphs(result.text);
    return { text: result.text, fragments: pages };
  }
  throw new Error("Alleen PDF-, DOCX- en TXT-bestanden zijn toegestaan.");
}

export function paragraphs(text: string): ExtractedFragment[] {
  return text.split(/\n\s*\n|\n/).map(s => s.trim()).filter(Boolean).map((text, i) => ({ text, location: `Alinea ${i + 1}` }));
}
