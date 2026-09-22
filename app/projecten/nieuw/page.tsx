import Link from "next/link";
import { randomUUID } from "node:crypto";
import { createPythonProjectAction } from "@/app/projecten/nieuw/actions";
import { SubmitButton } from "@/components/submit-button";

export default function NewProjectPage() {
  return <main className="shell" style={{maxWidth:1020}}><section className="page-head"><div><div className="eyebrow">Nieuw dossier</div><h1 style={{marginTop:10}}>Leg de context één keer goed vast.</h1><p>Deze gegevens worden gebruikt om scopeverschillen bij bewijsstukken zichtbaar te maken.</p></div><div style={{textAlign:"right"}}><Link href="/" className="button button-secondary">Terug naar dashboard</Link></div></section>
    <form action={createPythonProjectAction} className="panel panel-pad form-stack">
      <input type="hidden" name="idempotencyKey" value={randomUUID()}/>
      <div className="grid-2"><Field name="name" label="Projectnaam" required placeholder="AI-planningssoftware Gemeente Waterdam"/><Field name="client" label="Opdrachtgever" required placeholder="Gemeente Waterdam"/><Field name="reference" label="Aanbestedingsnummer of referentie" placeholder="WD-2026-041"/><Field name="dueDate" label="Uiterste inleverdatum" type="date"/><Field name="product" label="Aangeboden product of dienst" placeholder="Planwijzer AI"/><Field name="productVersion" label="Productversie" placeholder="2.3"/><Field name="owner" label="Verantwoordelijke medewerker" placeholder="Eva de Vries"/></div>
      <div className="field"><label htmlFor="notes">Optionele toelichting</label><textarea id="notes" name="notes" placeholder="Context, afbakening of afspraken voor dit dossier."/></div>
      <div style={{display:"flex",justifyContent:"flex-end",gap:10}}><Link href="/" className="button button-secondary">Annuleren</Link><SubmitButton pending="Dossier aanmaken…">Dossier aanmaken</SubmitButton></div>
    </form>
  </main>;
}
function Field({name,label,type="text",placeholder,required=false}:{name:string;label:string;type?:string;placeholder?:string;required?:boolean}) { return <div className="field"><label htmlFor={name}>{label}{required ? " *" : ""}</label><input id={name} name={name} type={type} placeholder={placeholder} required={required}/></div> }
