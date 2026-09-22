"use client";
import { useFormStatus } from "react-dom";
export function SubmitButton({ children, pending = "Bezig…", className = "button button-primary" }: { children: React.ReactNode; pending?: string; className?: string }) {
  const { pending: isPending } = useFormStatus();
  return <button className={className} disabled={isPending}>{isPending ? pending : children}</button>;
}

export function ConfirmButton({ children, message = "Weet u zeker dat u dit wilt verwijderen?" }: { children: React.ReactNode; message?: string }) {
  return <button className="button button-danger button-small" type="submit" onClick={e => { if (!window.confirm(message)) e.preventDefault(); }}>{children}</button>;
}

