import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";
import { PRODUCT } from "@/lib/config/product";

export const metadata: Metadata = { title: PRODUCT.metadataTitle, description: PRODUCT.description };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="nl"><body>
    <header className="topbar"><div className="topbar-inner"><Link href="/" className="brand"><span className="brand-mark" aria-hidden="true" />{PRODUCT.name}</Link><nav className="topnav" aria-label="Hoofdnavigatie"><Link href={PRODUCT.routes.uitleg} className="topnav-link">Voor wie</Link><Link href={PRODUCT.routes.dossiers} className="topnav-link">Dossiers</Link><Link href={PRODUCT.routes.demo} className="topnav-link topnav-accent">Demo-modus</Link><Link href={PRODUCT.routes.pitch} className="topnav-link">Investeerders</Link></nav><span className="muted topbar-context" style={{ fontSize: 12 }}>Demo-identiteit · {PRODUCT.demo.identity}</span></div></header>
    {children}
    <footer className="footer">Lokale MVP — niet bedoeld als productieklare beveiligings- of complianceomgeving.</footer>
  </body></html>;
}
