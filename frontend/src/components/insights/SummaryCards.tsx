import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { formatCompactMoney, formatMoney, formatNumber } from "@/lib/format";
import type { Summary } from "@/lib/types";

export function SummaryCards({ summary }: { summary?: Summary }) {
  const items = summary
    ? [
        { label: "Headcount", value: formatNumber(summary.headcount), hint: `${summary.countries} countries` },
        { label: "Total payroll (annual)", value: formatCompactMoney(summary.total_payroll, summary.currency), hint: `≈ ${summary.currency}, static FX` },
        { label: "Average salary", value: formatMoney(Math.round(summary.avg_salary), summary.currency), hint: summary.currency },
        { label: "Median salary", value: formatMoney(Math.round(summary.median_salary), summary.currency), hint: summary.currency },
      ]
    : [];
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {summary
        ? items.map((i) => (
            <Card key={i.label}>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">{i.label}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-semibold">{i.value}</div>
                <p className="text-xs text-muted-foreground">{i.hint}</p>
              </CardContent>
            </Card>
          ))
        : Array.from({ length: 4 }, (_, i) => <Skeleton key={i} className="h-28" />)}
    </div>
  );
}
