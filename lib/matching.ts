export function expiryState(expiresAt: Date | string | null, now = new Date()) {
  if (!expiresAt) return "geldig";
  const expiry = expiresAt instanceof Date ? expiresAt : new Date(`${expiresAt}T12:00:00`);
  if (expiry < now) return "verlopen";
  if (expiry.getTime() - now.getTime() <= 30 * 86_400_000) return "verloopt binnenkort";
  return "geldig";
}
