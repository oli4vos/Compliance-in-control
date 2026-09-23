import Link from "next/link";
import { ArrowRight, CheckCircle, Eye, ShieldCheck, UserCircle } from "@phosphor-icons/react/dist/ssr";
import { resetDemoAction } from "./actions";
import { PRODUCT } from "@/lib/config/product";

export default function DemoPage() {
  return <main className="shell demo-shell">
    <section className="demo-hero"><div><div className="eyebrow">{PRODUCT.name} / transparante demo</div><h1>Stap in als dossierbeheerder.</h1><p>Bekijk een volledig synthetisch dossier voor Planwijzer AI en volg één eis van bronfragment tot menselijke beslissing.</p></div><div className="demo-label"><span className="demo-label-dot" /> DEMO-MODUS<br /><small>Geen echte account of klantdata</small></div></section>
    <section className="demo-grid">
      <div className="panel demo-identity"><div className="demo-avatar"><UserCircle size={32} weight="duotone" /></div><div><span className="eyebrow">Demo-identiteit</span><h2>{PRODUCT.demo.identity}</h2><p className="muted">{PRODUCT.demo.role} · {PRODUCT.demo.organization}</p></div><span className="demo-active">Actief</span><div className="demo-identity-note"><ShieldCheck size={18} /> Deze identiteit is alleen voor de lokale demonstratie. Er wordt geen echte login of autorisatie gesimuleerd.</div><Link className="button button-primary" href="/projecten/demo-waterdam?tab=matrix">Open eisen-bewijsmatrix <ArrowRight size={17} /></Link></div>
      <div className="demo-guide"><div className="eyebrow">Wat u kunt testen</div><h2>Een geloofwaardige productroute in tien minuten.</h2><ol><li><span>Bron</span><div><strong>Bron bekijken</strong><small>Open de eisen en herleid iedere eis naar document en sectie.</small></div></li><li><span>Voorstel</span><div><strong>Voorstel controleren</strong><small>Bekijk letterlijk bewijs, score en waarschuwingen over scope of geldigheid.</small></div></li><li><span>Beslissing</span><div><strong>Menselijk beslissen</strong><small>Leg status, eigenaar, deadline en conceptantwoord vast.</small></div></li><li><span>Export</span><div><strong>Dossier exporteren</strong><small>Open de afdrukbare weergave of download de CSV-matrix.</small></div></li></ol></div>
    </section>
    <section className="demo-bottom"><div className="notice"><Eye size={19} /> Demo-data is synthetisch. De applicatie claimt geen certificering, juridische naleving of goedkeuring.</div><form action={resetDemoAction}><button className="button button-secondary" type="submit"><CheckCircle size={17} /> Demo terugzetten naar beginsituatie</button></form></section>
  </main>;
}
