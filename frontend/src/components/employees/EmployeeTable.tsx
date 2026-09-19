"use client";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { formatMoney } from "@/lib/format";
import type { Employee, SortField } from "@/lib/types";

interface Props {
  employees?: Employee[];
  loading: boolean;
  sortBy: SortField;
  order: "asc" | "desc";
  onSort: (field: SortField) => void;
  onEdit: (e: Employee) => void;
  onDelete: (e: Employee) => void;
  countryName: (code: string) => string;
}

const COLUMNS: { field: SortField; label: string; align?: "right" }[] = [
  { field: "full_name", label: "Name" },
  { field: "job_title", label: "Job title" },
  { field: "department", label: "Department" },
  { field: "country", label: "Country" },
  { field: "salary", label: "Annual salary", align: "right" },
  { field: "hire_date", label: "Hired" },
];

export function EmployeeTable({ employees, loading, sortBy, order, onSort, onEdit, onDelete, countryName }: Props) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          {COLUMNS.map((c) => (
            <TableHead
              key={c.field}
              className={c.align === "right" ? "text-right" : undefined}
              aria-sort={sortBy === c.field ? (order === "asc" ? "ascending" : "descending") : "none"}
            >
              <button type="button" className="inline-flex items-center gap-1 font-medium hover:underline" onClick={() => onSort(c.field)}>
                {c.label}
                <span aria-hidden className="text-xs text-muted-foreground">
                  {sortBy === c.field ? (order === "asc" ? "▲" : "▼") : ""}
                </span>
              </button>
            </TableHead>
          ))}
          <TableHead className="w-32" />
        </TableRow>
      </TableHeader>
      <TableBody>
        {!employees && loading
          ? Array.from({ length: 8 }, (_, i) => (
              <TableRow key={i}>
                <TableCell colSpan={COLUMNS.length + 1}>
                  <Skeleton className="h-5" />
                </TableCell>
              </TableRow>
            ))
          : employees?.map((e) => (
              <TableRow key={e.id} className={loading ? "opacity-60" : undefined}>
                <TableCell>
                  <div className="font-medium">{e.full_name}</div>
                  <div className="text-xs text-muted-foreground">{e.email}</div>
                </TableCell>
                <TableCell>{e.job_title}</TableCell>
                <TableCell>{e.department}</TableCell>
                <TableCell>{countryName(e.country)}</TableCell>
                <TableCell className="text-right tabular-nums">{formatMoney(e.salary, e.currency)}</TableCell>
                <TableCell className="tabular-nums">{e.hire_date}</TableCell>
                <TableCell className="text-right">
                  <Button variant="ghost" size="sm" onClick={() => onEdit(e)} aria-label={`Edit ${e.full_name}`}>Edit</Button>
                  <Button variant="ghost" size="sm" onClick={() => onDelete(e)} aria-label={`Delete ${e.full_name}`}>Delete</Button>
                </TableCell>
              </TableRow>
            ))}
        {employees?.length === 0 && (
          <TableRow>
            <TableCell colSpan={COLUMNS.length + 1} className="py-10 text-center text-muted-foreground">
              No employees match these filters.
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  );
}
