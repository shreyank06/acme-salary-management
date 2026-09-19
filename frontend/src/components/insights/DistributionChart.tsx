import { formatCompactMoney } from "@/lib/format";
import type { Distribution } from "@/lib/types";

/** Dependency-free horizontal histogram; accessible via the per-bar label. */
export function DistributionChart({ data }: { data: Distribution }) {
  const max = Math.max(1, ...data.buckets.map((b) => b.count));
  if (data.buckets.length === 0) return <p className="text-sm text-muted-foreground">No data.</p>;
  return (
    <ul className="space-y-1.5" aria-label="Salary distribution">
      {data.buckets.map((b) => (
        <li key={`${b.start}-${b.end}`} className="grid grid-cols-[9rem_1fr_3.5rem] items-center gap-3 text-xs">
          <span className="text-muted-foreground tabular-nums">
            {formatCompactMoney(b.start, data.currency)} – {formatCompactMoney(b.end, data.currency)}
          </span>
          <div className="h-4 rounded bg-muted">
            <div
              className="h-4 rounded bg-primary"
              style={{ width: `${(b.count / max) * 100}%` }}
              role="presentation"
            />
          </div>
          <span className="text-right tabular-nums">{b.count}</span>
        </li>
      ))}
    </ul>
  );
}
