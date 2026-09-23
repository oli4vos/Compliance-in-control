import Link from "next/link";
import { ArrowRight, Archive, CheckCircle, FileMagnifyingGlass, Handshake, Scales, UsersThree } from "@phosphor-icons/react/dist/ssr";
import { PRODUCT } from "@/lib/config/product";

const audiences = [
  { icon: UsersThree, title: "IT- en AI-leveranciers", text: "Voor teams die regelmatig aanbestedingen, securityreviews en klantvragen beantwoorden en bewijs steeds opnieuw moeten terugvinden." },
  { icon: Scales, title: "Security, privacy en AI-verantwoordelijken", text: "Voor inhoudelijke eigenaars die willen zien welke bron een eis ondersteunt, waar het bewijs tekortschiet en welke beslissing nog openstaat." },
  { icon: Handshake, title: "Sales- en aanbestedingsteams", text: "Voor medewerkers die sneller een controleerbaar dossier willen samenstellen zonder te beloven dat de tool juridische naleving vaststelt." },
];

const steps = [
  { title: "Leg de uitvraag vast", text: "Upload PDF, DOCX of TXT. IPC houdt document, locatie en letterlijk bronfragment bij.", icon: FileMagnifyingGlass },
  { title: "Maak eisen bespreekbaar", text: "Laat concept-eisen herkennen, bewerk ze waar nodig en markeer wat niet van toepassing is.", icon: Archive },
  { title: "Koppel bewijs met context", text: "Bekijk mogelijke bewijsstukken met fragment, score en waarschuwingen over scope, versie en geldigheid.", icon: CheckCircle },
  { title: "Laat de eigenaar beslissen", text: "Leg status, conceptantwoord, eigenaar, deadline en auditspoor vast. De mens bepaalt de uitkomst.", icon: Handshake },
];

export default function UitlegPage() {
  return <main className="shell explain-page">
    <section className="explain-hero">
      <div>
        <div className="eyebrow">Voor wie en hoe werkt het</div>
        <h1>Van losse bewijsstukken naar een dossier waar je op kunt werken.</h1>
        <p className="explain-lead">{PRODUCT.name} helpt Nederlandse IT- en AI-leveranciers om eisen, bronfragmenten, bewijsstukken en menselijke beoordelingen bij elkaar te houden. Zodat je team weet wat er ligt, wat nog ontbreekt en wie de volgende stap zet.</p>
        <div className="explain-actions"><Link className="button button-primary" href={PRODUCT.routes.demo}>Bekijk de demo <ArrowRight size={17} /></Link><Link className="text-link" href={PRODUCT.routes.dossiers}>Open de werkruimte</Link></div>
      </div>
      <aside className="explain-aside"><span className="mono">IPC / WERKWIJZE</span><strong>Bron eerst.<br />Mens beslist.</strong><p>Automatische voorstellen helpen zoeken. Ze vervangen geen beoordeling, certificering of juridisch oordeel.</p></aside>
    </section>

    <section className="explain-section"><div className="section-index">Voor wie</div><div><h2>Een werklaag voor teams die bewijs moeten verantwoorden.</h2><div className="audience-list">{audiences.map(({icon: Icon, title, text}) => <article key={title}><Icon size={24} weight="duotone" /><div><h3>{title}</h3><p>{text}</p></div></article>)}</div></div></section>

    <section className="explain-section explain-workflow"><div className="section-index">Zo werkt het</div><div><h2>Vier overzichtelijke handelingen, één traceerbaar dossier.</h2><div className="workflow-list">{steps.map(({title, text, icon: Icon}, index) => <article key={title}><span className="workflow-index">{String(index + 1).padStart(2, "0")}</span><Icon size={23} weight="duotone" /><div><h3>{title}</h3><p>{text}</p></div></article>)}</div></div></section>

    <section className="explain-section explain-relief"><div className="section-index">Zo ontzorgen we</div><div className="relief-grid"><div><h2>Minder zoeken. Minder contextverlies. Meer rust in de review.</h2><p>IPC neemt niet de verantwoordelijkheid over. Het maakt het voorbereidende werk overzichtelijker, zodat inhoudelijke eigenaars hun tijd besteden aan beoordelen in plaats van aan graven in oude mappen en spreadsheets.</p></div><div className="relief-points"><p><CheckCircle size={19} /> Iedere eis houdt een bron en locatie</p><p><CheckCircle size={19} /> Ieder voorstel toont letterlijk bewijs</p><p><CheckCircle size={19} /> Iedere beslissing krijgt eigenaar en auditspoor</p><p><CheckCircle size={19} /> Ieder exportdossier blijft duidelijk over hiaten</p></div></div></section>

    <section className="explain-bottom"><div><div className="eyebrow">Begin klein</div><h2>Volg één eis van bronfragment tot beslissing.</h2><p>De demo gebruikt synthetische gegevens en laat de volledige productroute zien.</p></div><Link className="button button-primary" href={PRODUCT.routes.demo}>Start de interactieve demo <ArrowRight size={17} /></Link></section>
    <div className="notice explain-disclaimer">{PRODUCT.disclaimer}</div>
  </main>;
}
