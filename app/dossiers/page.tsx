import Link from "next/link";
import { listProjects, type ProjectResponse } from "@/lib/api/client";

export const dynamic = "force-dynamic";

export default async function DossiersPage() {
  let projects: ProjectResponse[] = [];
  let backendError = "";
  try {
    projects = await listProjects();
  } catch (error) {
    backendError = error instanceof Error ? error.message : "De Python-backend is niet bereikbaar.";
  }
  return <main className="shell">
    <section className="hero"><div className="hero-copy"><div className="eyebrow">Compliance evidence workspace</div><h1 style={{ marginTop: 12 }}>Van uitvraag naar aantoonbaar dossier.</h1><p>Voor IT- en AI-leveranciers die bewijs willen terugvinden voordat een aanbesteding, securityreview of klantvraag vastloopt.</p><div className="hero-actions"><Link href="/projecten/nieuw" className="button button-primary">Nieuw dossier</Link><Link href="/demo" className="text-link">Start de demo <span aria-hidden="true">↗</span></Link></div><div className="hero-note"><span className="pulse-dot" /> Lokale demoomgeving · geen externe API vereist</div></div><div className="hero-aside"><div className="hero-stamp">IPC<br /><span>bewijs eerst</span></div><div className="hero-quote">“Een automatische match is een voorstel. De beslissing blijft bij de mens.”</div></div></section>
    <section className="investor-strip"><div><div className="eyebrow">Werkruimte</div><h2>De bewijslaag tussen AI-product en inkoopbesluit</h2><p>Elke nieuwe uitvraag hergebruikt dezelfde gecontroleerde bewijsbibliotheek. Dat maakt voorbereiding sneller, risico’s zichtbaarder en dossiers overdraagbaar.</p></div><div className="signal-grid"><div><strong className="mono">11</strong><span>demo-eisen</span></div><div><strong className="mono">7</strong><span>bewijsstukken</span></div><div><strong className="mono">3</strong><span>bewuste hiaten</span></div></div></section>
    <section className="panel"><div className="section-head panel-pad" style={{ paddingBottom: 8 }}><div><h2>Dossiers</h2><p className="muted" style={{ fontSize: 13, margin: "7px 0 0" }}>{projects.length} {projects.length === 1 ? "actief dossier" : "actieve dossiers"}</p></div><Link href="/projecten/nieuw" className="button button-secondary button-small">Nieuw dossier</Link></div>{backendError ? <div className="empty"><h3>Python-backend niet bereikbaar</h3><p>{backendError}</p><code>npm run dev:stack</code></div> : projects.length === 0 ? <div className="empty"><h3>Nog geen dossiers</h3><p>Maak een dossier aan om documenten en bewijs te verzamelen.</p><Link className="button button-primary" href="/projecten/nieuw">Eerste dossier aanmaken</Link></div> : projects.map(project => <Link href={`/projecten/${project.id}`} className="list-row project-link" key={project.id}><div><h3>{project.name}</h3><p className="muted" style={{ margin: "5px 0 0", fontSize: 12 }}>{project.client} · {project.reference || "Geen referentie"} · {project.product} {project.productVersion}</p></div><div><div className="mono" style={{ fontSize: 18, fontWeight: 700, color: "var(--navy)" }}>{project.progress}%</div><div className="progress"><span style={{ width: `${project.progress}%` }} /></div><span className="muted" style={{ fontSize: 10 }}>{project.sufficientCount} van {project.requirementCount} voldoende</span></div><div><span className="muted" style={{ fontSize: 11 }}>Eerstvolgende deadline</span><div style={{ fontSize: 13, marginTop: 4 }}>{formatDate(project.nextDeadline || project.dueDate)}</div></div></Link>)}</section>
  </main>;
}

function formatDate(value: string | null | undefined) { return value ? new Date(`${value.slice(0, 10)}T12:00:00`).toLocaleDateString("nl-NL") : "Niet vastgelegd"; }
