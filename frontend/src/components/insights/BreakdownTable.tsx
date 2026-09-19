import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { formatMoney, formatNumber } from "@/lib/format";
import type { BreakdownRow } from "@/lib/types";

interface Props {
  rows?: BreakdownRow[];
  keyLabel: string;
  renderKey?: (key: string) => string;
}

export function BreakdownTable({ rows, keyLabel, renderKey = (k) => k }: Props) {
  if (!rows) return <Skeleton className="h-64" />;
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>{keyLabel}</TableHead>
          <TableHead className="text-right">Headcount</TableHead>
          <TableHead className="text-right">Min</TableHead>
          <TableHead className="text-right">Median</TableHead>
          <TableHead className="text-right">Average</TableHead>
          <TableHead className="text-right">Max</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {rows.map((r) => (
          <TableRow key={r.key}>
            <TableCell className="font-medium">{renderKey(r.key)}</TableCell>
            <TableCell className="text-right tabular-nums">{formatNumber(r.stats.count)}</TableCell>
            <TableCell className="text-right tabular-nums">{formatMoney(r.stats.min, r.currency)}</TableCell>
            <TableCell className="text-right tabular-nums">{formatMoney(r.stats.median, r.currency)}</TableCell>
            <TableCell className="text-right tabular-nums">{formatMoney(Math.round(r.stats.avg), r.currency)}</TableCell>
            <TableCell className="text-right tabular-nums">{formatMoney(r.stats.max, r.currency)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
