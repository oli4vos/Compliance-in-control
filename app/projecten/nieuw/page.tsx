import Link from "next/link";
import { randomUUID } from "node:crypto";
import { createPythonProjectAction } from "@/app/projecten/nieuw/actions";
import { SubmitButton } from "@/components/submit-button";

export default function NewProjectPage() {
  return <main className="shell" style={{maxWidth:1020}}><section className="page-head"><div><div className="eyebrow">Nieuw dossier</div><h1 style={{marginTop:10}}>Leg de context één keer goed vast.</h1><p>Deze gegevens worden gebruikt om scopeverschillen bij bewijsstukken zichtbaar te maken.</p></div><div style={{textAlign:"right"}}><Link href="/dossiers" className="button button-secondary">Terug naar dossiers</Link></div></section>
    <form action={createPythonProjectAction} className="panel panel-pad form-stack">
      <input type="hidden" name="idempotencyKey" value={randomUUID()}/>
      <div className="form-intro"><span className="eyebrow">Eerste stap</span><h2>Maak de context van dit dossier herkenbaar.</h2><p>Je kunt documenten, eisen en bewijs later altijd aanvullen. Begin met wat je al zeker weet.</p></div>
      <fieldset className="form-section"><legend>Dossieridentiteit</legend><p className="form-help">Deze gegevens verschijnen op de matrix en in exports.</p><div className="grid-2"><Field name="name" label="Projectnaam" required placeholder="AI-planningssoftware Gemeente Waterdam"/><Field name="client" label="Opdrachtgever" required placeholder="Gemeente Waterdam"/><Field name="reference" label="Aanbestedingsnummer of referentie" placeholder="WD-2026-041"/><Field name="dueDate" label="Uiterste inleverdatum" type="date"/></div></fieldset>
      <fieldset className="form-section"><legend>Productscope</legend><p className="form-help">Zo kan IPC later waarschuwen wanneer bewijs niet op dezelfde versie of omgeving ziet.</p><div className="grid-2"><Field name="product" label="Aangeboden product of dienst" placeholder="Planwijzer AI"/><Field name="productVersion" label="Productversie" placeholder="2.3"/></div></fieldset>
      <fieldset className="form-section"><legend>Eigenaarschap</legend><p className="form-help">De verantwoordelijke bewaakt de voortgang; inhoudelijke beoordelingen kunnen later per eis worden toegewezen.</p><Field name="owner" label="Verantwoordelijke medewerker" placeholder="Eva de Vries"/><div className="field"><label htmlFor="notes">Toelichting <span className="muted">(optioneel)</span></label><textarea id="notes" name="notes" placeholder="Context, afbakening of afspraken voor dit dossier."/></div></fieldset>
      <div style={{display:"flex",justifyContent:"flex-end",gap:10}}><Link href="/dossiers" className="button button-secondary">Annuleren</Link><SubmitButton pending="Dossier aanmaken…">Dossier aanmaken</SubmitButton></div>
    </form>
  </main>;
}
function Field({name,label,type="text",placeholder,required=false}:{name:string;label:string;type?:string;placeholder?:string;required?:boolean}) { return <div className="field"><label htmlFor={name}>{label}{required ? " *" : ""}</label><input id={name} name={name} type={type} placeholder={placeholder} required={required}/></div> }
