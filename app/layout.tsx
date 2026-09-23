import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = { title: "Aantoonbaar — Bewijsdossiers", description: "Lokale werkruimte voor controleerbare eisen-bewijsmatrices." };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="nl"><body>
    <header className="topbar"><div className="topbar-inner"><Link href="/" className="brand"><span className="brand-mark" aria-hidden="true" />Aantoonbaar</Link><nav className="topnav" aria-label="Hoofdnavigatie"><Link href="/dossiers" className="topnav-link">Dossiers</Link><Link href="/demo" className="topnav-link topnav-accent">Demo-modus</Link><Link href="/pitch" className="topnav-link">Investeerders</Link></nav><span className="muted topbar-context" style={{ fontSize: 12 }}>Demo-identiteit · Eva de Vries</span></div></header>
    {children}
    <footer className="footer">Lokale MVP — niet bedoeld als productieklare beveiligings- of complianceomgeving.</footer>
  </body></html>;
}
