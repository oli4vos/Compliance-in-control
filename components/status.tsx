export function StatusBadge({ status }: { status: string }) {
  const cls = status === "voldoende onderbouwd" ? "status-good" : status === "gedeeltelijk onderbouwd" ? "status-partial" : ["ontbrekend bewijs", "onvoldoende onderbouwd"].includes(status) ? "status-bad" : status === "mogelijk passend" ? "status-proposal" : "status-neutral";
  return <span className={`badge ${cls}`}>{status}</span>;
}

export function ExpiryBadge({ state }: { state: string }) {
  const cls = state === "verlopen" ? "status-bad" : state === "verloopt binnenkort" ? "status-partial" : "status-good";
  return <span className={`badge ${cls}`}>{state}</span>;
}

