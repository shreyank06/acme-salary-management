"use client";

import { useState } from "react";
import { ErrorNotice } from "@/components/common/ErrorNotice";
import { FilterSelect } from "@/components/common/FilterSelect";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAsync } from "@/hooks/useAsync";
import { useReferenceData } from "@/hooks/useReferenceData";
import { api } from "@/lib/api";
import type { GroupBy } from "@/lib/types";
import { BreakdownTable } from "./BreakdownTable";
import { DistributionChart } from "./DistributionChart";
import { SummaryCards } from "./SummaryCards";

const GROUPS: { value: GroupBy; label: string }[] = [
  { value: "country", label: "Country" },
  { value: "department", label: "Department" },
  { value: "job_title", label: "Job title" },
];

export function InsightsView() {
  const { countries, countryName } = useReferenceData();
  const [country, setCountry] = useState("");
  const [groupBy, setGroupBy] = useState<GroupBy>("country");

  const scope = { country: country || undefined };
  const summary = useAsync(() => api.summary(scope), [country]);
  const breakdown = useAsync(() => api.breakdown(groupBy, country || undefined), [groupBy, country]);
  const distribution = useAsync(() => api.distribution(scope), [country]);

  const error = summary.error ?? breakdown.error ?? distribution.error;
  const reload = () => {
    summary.reload();
    breakdown.reload();
    distribution.reload();
  };
  const groupLabel = GROUPS.find((g) => g.value === groupBy)!.label;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">How we pay people</h1>
          <p className="text-sm text-muted-foreground">
            {country
              ? `Scoped to ${countryName(country)} — amounts in local currency.`
              : "Organisation-wide — amounts normalised to USD at static approximate rates."}
          </p>
        </div>
        <FilterSelect
          ariaLabel="Country scope"
          className="w-52"
          value={country}
          onChange={setCountry}
          allLabel="All countries"
          options={countries.map((c) => ({ value: c.code, label: c.name }))}
        />
      </div>

      {error && <ErrorNotice message={error} onRetry={reload} />}
      <SummaryCards summary={summary.data} />

      <Card>
        <CardHeader className="flex-row items-center justify-between gap-2">
          <CardTitle>Salary breakdown</CardTitle>
          <div className="flex gap-1" role="group" aria-label="Group by">
            {GROUPS.map((g) => (
              <Button
                key={g.value}
                size="sm"
                variant={g.value === groupBy ? "default" : "outline"}
                aria-pressed={g.value === groupBy}
                onClick={() => setGroupBy(g.value)}
              >
                {g.label}
              </Button>
            ))}
          </div>
        </CardHeader>
        <CardContent>
          <BreakdownTable
            rows={breakdown.data}
            keyLabel={groupLabel}
            renderKey={groupBy === "country" ? countryName : undefined}
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Salary distribution{distribution.data ? ` (${distribution.data.currency})` : ""}</CardTitle>
        </CardHeader>
        <CardContent>{distribution.data && <DistributionChart data={distribution.data} />}</CardContent>
      </Card>
    </div>
  );
}
