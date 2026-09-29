import Link from "next/link";
import { ArrowUpRight } from "@phosphor-icons/react/dist/ssr";
import { PRODUCT } from "@/lib/config/product";

export const dynamic = "force-dynamic";
export const metadata = {
  title: `Investeerderscase | ${PRODUCT.name}`,
  description: "De investeerderscase van IPC: probleem, bewijslaag, markttoegang, economie en validatieplan.",
};

const forecast = [
  ["Jaar 1", "Pilot en eerste hergebruik", "18", "€ 86k", "€ -74k"],
  ["Jaar 2", "Herhaalbaar in security en tenders", "65", "€ 364k", "€ -42k"],
  ["Jaar 3", "Partnerkanaal en teamlicenties", "145", "€ 1,04m", "+ € 182k"],
  ["Jaar 4", "Portfolio’s en meerdere disciplines", "310", "€ 2,48m", "+ € 690k"],
  ["Jaar 5", "Categorie voor aantoonbaarheid", "560", "€ 5,04m", "+ € 1,82m"],
];

export default function InvesteerdersPage() {
  return <main className="investor-page">
    <nav className="investor-nav" aria-label="Investeerderspagina">
      <Link className="investor-brand" href="/"><span className="brand-mark" aria-hidden="true" /><span><b>{PRODUCT.name}</b><small>investeerderscase</small></span></Link>
      <div className="investor-nav-links"><a href="#model">Model</a><a href="#markt">Markttoegang</a><a href="#economie">Economie</a><a href="#bewijsplan">Bewijsplan</a></div>
      <Link className="investor-product-link" href="/demo">Bekijk product <ArrowUpRight size={16} /></Link>
    </nav>

    <section className="investor-hero">
      <div className="investor-hero-copy"><p className="eyebrow">INVESTEERDERSCASE / MANAGEMENTAANNAMES</p><h1>Bewijs dat blijft werken voor leveranciers die AI verkopen.</h1><p className="investor-thesis">IPC maakt rommelige aanbestedingen, securityvragenlijsten en klantuitvragen controleerbaar. Automatische voorstellen versnellen het voorbereidende werk; de eigenaar van het bewijs blijft verantwoordelijk voor het besluit.</p><div className="investor-tags"><span>Evidence workspace</span><span>Human-in-the-loop</span><span>IT- en AI-leveranciers</span></div></div>
      <aside className="investment-ask"><span className="ask-label">INDICATIEVE PRE-SEED</span><strong>€ 300.000</strong><p>18 maanden om hergebruik, betalingsbereidheid en een reproduceerbare reviewworkflow met design partners te bewijzen.</p><div className="funding-split"><span><b>45%</b> product &amp; veiligheid</span><span><b>25%</b> distributie</span><span><b>20%</b> validatie</span><span><b>10%</b> operatie</span></div></aside>
    </section>

    <section className="investor-problem-model" id="model"><div className="investor-problem"><p className="eyebrow">HET PROBLEEM</p><h2>De schaarse tijd van security- en aanbestedingsteams verdwijnt in het ordenen van bewijs.</h2><p>Hetzelfde antwoord wordt opnieuw gezocht in policies, audits, model cards en spreadsheets. Daardoor blijft scope onduidelijk, worden hiaten laat ontdekt en is kennis moeilijk overdraagbaar.</p></div><div className="investor-model-steps"><div><b>01</b><span>De organisatie legt uitvraag en documenten vast.</span></div><div><b>02</b><span>IPC herkent concept-eisen en houdt bronfragmenten traceerbaar.</span></div><div><b>03</b><span>De lokale matcher stelt bewijs voor met fragment, score en waarschuwingen.</span></div><div><b>04</b><span>De eigenaar beoordeelt, plant opvolging en exporteert een onderbouwd dossier.</span></div></div></section>

    <section className="investor-market" id="markt"><div className="investor-market-copy"><p className="eyebrow">WAAROM NU / EERSTE MARKT</p><h2>Begin smal waar de vraag terugkomt en de waarde snel zichtbaar is.</h2><p>De eerste wedge is niet “compliance voor iedereen”, maar terugkerend bewijswerk bij Nederlandse IT- en AI-leveranciers. Elke nieuwe uitvraag gebruikt dezelfde bewijsbibliotheek, terwijl menselijke eigenaars de kwaliteit bewaken.</p></div><div className="investor-market-path"><article><span>01 / VRAAG</span><strong>Leveranciers met terugkerende uitvragen</strong><p>Start bij aanbestedingen, securityreviews en AI-vragenlijsten met korte deadlines.</p></article><article><span>02 / DISTRIBUTIE</span><strong>Security-, privacy- en aanbestedingspartners</strong><p>Partners brengen herhaalde workflows en vertrouwen mee, zonder brede acquisitie vanaf dag één.</p></article><article><span>03 / UITBREIDING</span><strong>Van dossier naar organisatiebrede bewijslaag</strong><p>Meer teams, producten en dossiers vergroten hergebruik en omzet per organisatie.</p></article></div></section>

    <section className="investor-economics" id="economie"><div className="section-head"><div><p className="eyebrow">UNIT ECONOMICS / BASISSCENARIO</p><h2>Omzet groeit met hergebruik, niet met een groter documententeam.</h2></div><p className="section-note">Werkhypothese: jaarlijkse workspace-licentie met team- en partneruitbreiding. Servicesomzet en churn zijn nog niet in deze indicatie opgenomen.</p></div><div className="metric-ribbon"><div><small>Gem. contractwaarde jaar 3</small><strong>€ 7.200</strong><span>per organisatie per jaar</span></div><div><small>Brutomarge-hypothese</small><strong>78%</strong><span>software en lokale extractie</span></div><div><small>Terugkerend hergebruik</small><strong>3,4×</strong><span>doel per bewijsstuk</span></div><div><small>Bijdrage per team</small><strong>€ 18k</strong><span>voor vaste kosten</span></div></div></section>

    <section className="investor-forecast"><div className="forecast-head"><div><p className="eyebrow">VIJFJARENPLAN</p><h2>Een toetsbaar pad naar € 5,0 mln. ARR.</h2><p>Gecontroleerde groei via hergebruik, teams en partnerdistributie.</p></div><div className="scenario-stamp">BASISSCENARIO<br /><b>indicatief</b></div></div><div className="forecast-table-wrap"><table className="forecast-table"><thead><tr><th>Periode</th><th>Focus</th><th>Klanten</th><th>ARR</th><th>Run-rate ruimte</th></tr></thead><tbody>{forecast.map(([year, focus, customers, arr, room]) => <tr key={year}><td><strong>{year}</strong></td><td><small>{focus}</small></td><td>{customers}</td><td className="arr-cell"><b>{arr}</b></td><td className={room.startsWith("+") ? "positive" : "negative"}>{room}</td></tr>)}</tbody></table></div><p className="forecast-footnote">ARR is een indicatieve annualisatie op basis van klanten en gemiddelde contractwaarde. Dit is geen boekhoudkundige winst, waardering of forecast.</p></section>

    <section className="investor-evidence" id="bewijsplan"><div><p className="eyebrow">FASE VAN HET BEDRIJF</p><h2>Werkend productconcept; commerciële aannames nog te bewijzen.</h2></div><dl className="evidence-ledger"><div><dt>Gebouwd</dt><dd>End-to-end demo van intake, eisenextractie, matching, menselijke beoordeling en export.</dd></div><div><dt>Te valideren</dt><dd>Betalingsbereidheid, hergebruik per dossier, reviewtijd en partnerdistributie.</dd></div><div><dt>Investeringspoort</dt><dd>Pas opschalen wanneer klantwaarde én bijdrage per organisatie reproduceerbaar zijn.</dd></div></dl></section>

    <section className="investor-milestones"><div><p className="eyebrow">UITVOERINGSPLAN</p><h2>Bewijs vóór schaal.</h2><div className="milestones"><div><b>0—12 maanden</b><strong>Workflow bewijzen</strong><span>8 design partners, 50 actieve dossiers en tijd tot eerste beoordeling meten.</span></div><div><b>12—24 maanden</b><strong>Distributie bewijzen</strong><span>Security- en aanbestedingspartners aansluiten; hergebruik per bewijsstuk aantonen.</span></div><div><b>24—36 maanden</b><strong>Organisatie uitbreiden</strong><span>Van losse dossiers naar meerdere teams, producten en terugkerende klantuitvragen.</span></div></div></div><section className="defensibility"><p className="eyebrow">VERDEDIGBAARHEID</p><h2>De voorsprong zit in workflowdata, niet in één model.</h2><ul><li><b>Traceerbare bewijsdata</b><span>Bronnen, fragmenten, scopes en beslissingen worden herbruikbaar.</span></li><li><b>Menselijke kwaliteitslaag</b><span>Iedere definitieve status blijft gekoppeld aan een eigenaar en auditspoor.</span></li><li><b>Operationele leercurve</b><span>Elke review verbetert intake, matching en opvolging.</span></li></ul></section></section>

    <section className="investor-risks"><div><p className="eyebrow">BELANGRIJKSTE RISICO’S</p><h2>Investeer op meetpunten, niet op optimisme.</h2></div><div className="risk-list"><article><b>Adoptie</b><p>Meet of teams een dossier echt hergebruiken voordat uitbreiding wordt verkocht.</p></article><article><b>Datakwaliteit</b><p>Bronfragmenten, scope en geldigheid blijven zichtbaar; zwakke matches worden niet als besluit opgeslagen.</p></article><article><b>Distributie</b><p>Bewijs partnerkanaal eerst met enkele gespecialiseerde security- en aanbestedingspartijen.</p></article><article><b>Positionering</b><p>IPC ondersteunt voorbereiding en beoordeling, maar claimt geen certificering of juridisch oordeel.</p></article></div></section>

    <aside className="assumption-banner"><b>Dit is een pitchmodel, geen voorspelling.</b><span>Alle bedragen, volumes en mijlpalen zijn managementaannames voor discussie en moeten met pilots, interviews en echte conversiedata worden gevalideerd.</span></aside>
    <section className="investor-close"><p className="eyebrow">DE INVESTERINGSTHESE</p><h2>Maak bewijswerk herbruikbaar — en geef teams tijd terug voor de beoordeling die er echt toe doet.</h2><div><span>Indicatieve ronde</span><strong>€ 300.000 pre-seed</strong><small>Onder voorbehoud van pilotvalidatie, security review en definitieve begroting.</small></div><Link className="button button-primary" href="/demo">Bekijk het werkende product <ArrowUpRight size={17} /></Link></section>
  </main>;
}
