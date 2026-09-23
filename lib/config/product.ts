/** Publieke productconfiguratie voor alle Next.js-schermen.
 *
 * Houd publieke copy hier centraal. Secrets, database-URL's en backend-runtime
 * horen in de Python settingslaag en mogen nooit in deze module terechtkomen.
 */
export const PRODUCT = {
  name: "IPC",
  description: "Lokale werkruimte voor controleerbare eisen-bewijsmatrices.",
  metadataTitle: "IPC — Bewijsdossiers",
  disclaimer:
    "IPC ondersteunt de voorbereiding en beoordeling van bewijsdossiers. Een voorgestelde koppeling is geen juridisch oordeel, certificering of garantie van naleving.",
  demo: {
    identity: "Eva de Vries",
    role: "Dossierbeheerder",
    organization: "Planwijzer Systemen B.V.",
  },
  routes: {
    dossiers: "/dossiers",
    demo: "/demo",
    pitch: "/pitch",
  },
  features: {
    demoMode: true,
    localExtraction: true,
    optionalLlm: true,
  },
} as const;
