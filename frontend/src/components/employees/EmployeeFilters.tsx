"use client";

import { FilterSelect } from "@/components/common/FilterSelect";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import type { Country, Facets } from "@/lib/types";

export interface FilterState {
  q: string;
  country: string;
  department: string;
  job_title: string;
  min_salary: string;
  max_salary: string;
}

export const EMPTY_FILTERS: FilterState = {
  q: "",
  country: "",
  department: "",
  job_title: "",
  min_salary: "",
  max_salary: "",
};

interface Props {
  value: FilterState;
  onChange: (next: FilterState) => void;
  countries: Country[];
  facets: Facets;
}

export function EmployeeFilters({ value, onChange, countries, facets }: Props) {
  const set = (patch: Partial<FilterState>) => onChange({ ...value, ...patch });
  const opts = (xs: string[]) => xs.map((x) => ({ value: x, label: x }));
  const dirty = JSON.stringify(value) !== JSON.stringify(EMPTY_FILTERS);
  return (
    <div className="flex flex-wrap items-center gap-2">
      <Input
        aria-label="Search employees"
        placeholder="Search name or email…"
        className="w-64"
        value={value.q}
        onChange={(e) => set({ q: e.target.value })}
      />
      <FilterSelect ariaLabel="Country" className="w-44" value={value.country} onChange={(v) => set({ country: v })}
        allLabel="All countries" options={countries.map((c) => ({ value: c.code, label: c.name }))} />
      <FilterSelect ariaLabel="Department" className="w-44" value={value.department} onChange={(v) => set({ department: v })}
        allLabel="All departments" options={opts(facets.departments)} />
      <FilterSelect ariaLabel="Job title" className="w-52" value={value.job_title} onChange={(v) => set({ job_title: v })}
        allLabel="All job titles" options={opts(facets.job_titles)} />
      <Input aria-label="Minimum salary" type="number" min={0} placeholder="Min salary" className="w-32"
        value={value.min_salary} onChange={(e) => set({ min_salary: e.target.value })} />
      <Input aria-label="Maximum salary" type="number" min={0} placeholder="Max salary" className="w-32"
        value={value.max_salary} onChange={(e) => set({ max_salary: e.target.value })} />
      {dirty && (
        <Button variant="ghost" size="sm" onClick={() => onChange(EMPTY_FILTERS)}>
          Clear
        </Button>
      )}
    </div>
  );
}
