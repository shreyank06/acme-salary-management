/** Shown when the first load is slow; the free-tier API sleeps when idle and takes ~50s to wake. */
export function SlowServerNotice({ show }: { show: boolean }) {
  if (!show) return null;
  return (
    <div role="status" className="rounded-lg border bg-muted/50 p-4 text-sm">
      Waking up the server — the demo API sleeps when idle, so the first load can take up to a minute.
    </div>
  );
}
