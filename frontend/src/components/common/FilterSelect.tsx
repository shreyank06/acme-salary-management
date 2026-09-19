"use client";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export interface Option {
  value: string;
  label: string;
}

interface Props {
  value: string;
  onChange: (value: string) => void;
  options: Option[];
  /** Label of the "no filter" entry, e.g. "All countries". Omit for required selects. */
  allLabel?: string;
  ariaLabel: string;
  className?: string;
}

const ALL = "__all__";

export function FilterSelect({ value, onChange, options, allLabel, ariaLabel, className }: Props) {
  const items = allLabel ? [{ value: ALL, label: allLabel }, ...options] : options;
  return (
    <Select
      items={items}
      value={value === "" && allLabel ? ALL : value}
      onValueChange={(v) => onChange(v === ALL || v === null ? "" : String(v))}
    >
      <SelectTrigger aria-label={ariaLabel} className={className}>
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        {items.map((o) => (
          <SelectItem key={o.value} value={o.value}>
            {o.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
