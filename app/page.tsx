import Link from "next/link";
import { db } from "@/lib/db";
import { DISCLAIMER } from "@/lib/constants";

export const dynamic = "force-dynamic";
export default async function Dashboard() {
  const projects = await db.project.findMany({ orderBy: { createdAt: "desc" }, include: { requirements: true, tasks: { where: { status: "open" } }, evidenceDocuments: true } });
  return <main className="shell">
    <section className="hero"><div className="hero-copy"><div className="eyebrow">Compliance evidence workspace</div><h1 style={{marginTop:12}}>Van uitvraag naar aantoonbaar dossier.</h1><p>Voor IT- en AI-leveranciers die bewijs willen terugvinden voordat een aanbesteding, securityreview of klantvraag vastloopt.</p><div className="hero-actions"><Link href="/projecten/nieuw" className="button button-primary">Nieuw dossier</Link><Link href="/pitch" className="text-link">Bekijk de businesscase <span aria-hidden="true">↗</span></Link></div><div className="hero-note"><span className="pulse-dot"/> Lokale demoomgeving · geen externe API vereist</div></div><div className="hero-aside"><div className="hero-stamp">AANTOONBAAR<br/><span>bewijs eerst</span></div><div className="hero-quote">“Een automatische match is een voorstel. De beslissing blijft bij de mens.”</div></div></section>
    <div className="notice" style={{marginBottom:22}}>{DISCLAIMER}</div>
    <section className="investor-strip"><div><div className="eyebrow">Waarom nu</div><h2>De bewijslaag tussen AI-product en inkoopbesluit</h2><p>Elke nieuwe uitvraag hergebruikt dezelfde gecontroleerde bewijsbibliotheek. Dat maakt voorbereiding sneller, risico’s zichtbaarder en dossiers overdraagbaar.</p></div><div className="signal-grid"><div><strong className="mono">11</strong><span>demo-eisen</span></div><div><strong className="mono">7</strong><span>bewijsstukken</span></div><div><strong className="mono">3</strong><span>bewuste hiaten</span></div></div></section>
    <section className="panel">
      <div className="section-head panel-pad" style={{paddingBottom:8}}><div><h2>Dossiers</h2><p className="muted" style={{fontSize:13,margin:"7px 0 0"}}>{projects.length} {projects.length === 1 ? "actief dossier" : "actieve dossiers"}</p></div></div>
      {projects.length === 0 ? <div className="empty"><h3>Nog geen dossiers</h3><p>Maak een dossier aan om documenten en bewijs te verzamelen.</p><Link className="button button-primary" href="/projecten/nieuw">Eerste dossier aanmaken</Link></div> : projects.map(project => {
        const reviewed = project.requirements.filter(r => r.status !== "niet beoordeeld" && r.status !== "mogelijk passend").length;
        const sufficient = project.requirements.filter(r => r.status === "voldoende onderbouwd").length;
        const progress = project.requirements.length ? Math.round(reviewed / project.requirements.length * 100) : 0;
        const next = project.tasks.filter(t => t.deadline).sort((a,b) => +a.deadline! - +b.deadline!)[0];
        return <Link href={`/projecten/${project.id}`} className="list-row project-link" key={project.id}><div><h3>{project.name}</h3><p className="muted" style={{margin:"5px 0 0",fontSize:12}}>{project.client} · {project.reference || "Geen referentie"} · {project.product} {project.productVersion}</p></div><div><div className="mono" style={{fontSize:18,fontWeight:700,color:"var(--navy)"}}>{progress}%</div><div className="progress"><span style={{width:`${progress}%`}}/></div><span className="muted" style={{fontSize:10}}>{sufficient} van {project.requirements.length} voldoende</span></div><div><span className="muted" style={{fontSize:11}}>Eerstvolgende deadline</span><div style={{fontSize:13,marginTop:4}}>{next?.deadline ? next.deadline.toLocaleDateString("nl-NL") : project.dueDate?.toLocaleDateString("nl-NL") || "Niet vastgelegd"}</div></div></Link>;
      })}
    </section>
  </main>;
}
