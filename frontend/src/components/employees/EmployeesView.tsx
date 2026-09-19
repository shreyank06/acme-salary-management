"use client";

import { useState } from "react";
import { toast } from "sonner";
import { ErrorNotice } from "@/components/common/ErrorNotice";
import { SlowServerNotice } from "@/components/common/SlowServerNotice";
import { Button } from "@/components/ui/button";
import { useAsync } from "@/hooks/useAsync";
import { useDelayedFlag } from "@/hooks/useDelayedFlag";
import { useDebounce } from "@/hooks/useDebounce";
import { useReferenceData } from "@/hooks/useReferenceData";
import { api } from "@/lib/api";
import type { Employee, EmployeeQuery, SortField } from "@/lib/types";
import { DeleteEmployeeDialog } from "./DeleteEmployeeDialog";
import { EmployeeFilters, EMPTY_FILTERS, type FilterState } from "./EmployeeFilters";
import { EmployeeFormDialog } from "./EmployeeFormDialog";
import { EmployeeTable } from "./EmployeeTable";
import { Pagination } from "./Pagination";

const PAGE_SIZE = 25;
const toInt = (s: string) => (s === "" ? undefined : Number(s));

export function EmployeesView() {
  const { countries, facets, countryName } = useReferenceData();
  const [filters, setFilters] = useState<FilterState>(EMPTY_FILTERS);
  const [sortBy, setSortBy] = useState<SortField>("full_name");
  const [order, setOrder] = useState<"asc" | "desc">("asc");
  const [page, setPage] = useState(1);
  const [formTarget, setFormTarget] = useState<Employee | "new" | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Employee | null>(null);

  // Debounce the whole filter object so typing doesn't fire a request per keystroke.
  const debounced = useDebounce(filters, 300);

  const query: EmployeeQuery = {
    q: debounced.q.trim(),
    country: debounced.country,
    department: debounced.department,
    job_title: debounced.job_title,
    min_salary: toInt(debounced.min_salary),
    max_salary: toInt(debounced.max_salary),
    sort_by: sortBy,
    order,
    page,
    page_size: PAGE_SIZE,
  };
  const { data, error, loading, reload } = useAsync(() => api.listEmployees(query), [query]);

  const slow = useDelayedFlag(loading && !data && !error, 4000);

  // Any change to filters/sort goes back to page 1 (done in handlers, not in an effect).
  function changeFilters(next: FilterState) {
    setFilters(next);
    setPage(1);
  }

  function toggleSort(field: SortField) {
    if (field === sortBy) setOrder((o) => (o === "asc" ? "desc" : "asc"));
    else {
      setSortBy(field);
      setOrder("asc");
    }
    setPage(1);
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold tracking-tight">Employees</h1>
        <Button onClick={() => setFormTarget("new")}>Add employee</Button>
      </div>
      <EmployeeFilters value={filters} onChange={changeFilters} countries={countries} facets={facets} />
      {error && <ErrorNotice message={error} onRetry={reload} />}
      <SlowServerNotice show={slow} />
      <EmployeeTable
        employees={data?.items}
        loading={loading}
        sortBy={sortBy}
        order={order}
        onSort={toggleSort}
        onEdit={setFormTarget}
        onDelete={setDeleteTarget}
        countryName={countryName}
      />
      {data && <Pagination page={data.page} pages={data.pages} total={data.total} pageSize={PAGE_SIZE} onPage={setPage} />}

      <EmployeeFormDialog
        target={formTarget}
        countries={countries}
        onClose={() => setFormTarget(null)}
        onSaved={(msg) => {
          setFormTarget(null);
          toast.success(msg);
          reload();
        }}
      />
      <DeleteEmployeeDialog
        employee={deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onDeleted={() => {
          setDeleteTarget(null);
          toast.success("Employee deleted");
          reload();
        }}
      />
    </div>
  );
}
