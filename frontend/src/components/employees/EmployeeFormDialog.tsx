"use client";

import { useState } from "react";
import { FilterSelect } from "@/components/common/FilterSelect";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api";
import type { Country, Employee, EmployeeInput } from "@/lib/types";
import { type FormErrors, validateEmployee } from "@/lib/validation";

interface Props {
  /** `null` = closed, `"new"` = create, an Employee = edit. */
  target: Employee | "new" | null;
  countries: Country[];
  onClose: () => void;
  onSaved: (message: string) => void;
}

const BLANK: EmployeeInput = {
  full_name: "", email: "", job_title: "", department: "", country: "", salary: 0, hire_date: "",
};

export function EmployeeFormDialog({ target, countries, onClose, onSaved }: Props) {
  return (
    <Dialog open={target !== null} onOpenChange={(open) => !open && onClose()}>
      <DialogContent>
        {/* keyed so form state resets whenever a different record is opened */}
        {target !== null && (
          <Form key={target === "new" ? "new" : target.id} target={target} countries={countries} onClose={onClose} onSaved={onSaved} />
        )}
      </DialogContent>
    </Dialog>
  );
}

function Form({ target, countries, onClose, onSaved }: Omit<Props, "target"> & { target: Employee | "new" }) {
  const editing = target !== "new" ? target : null;
  const [values, setValues] = useState<EmployeeInput>(
    editing
      ? { full_name: editing.full_name, email: editing.email, job_title: editing.job_title,
          department: editing.department, country: editing.country, salary: editing.salary, hire_date: editing.hire_date }
      : BLANK,
  );
  const [errors, setErrors] = useState<FormErrors>({});
  const [serverError, setServerError] = useState<string>();
  const [saving, setSaving] = useState(false);

  const set = <K extends keyof EmployeeInput>(key: K, value: EmployeeInput[K]) =>
    setValues((v) => ({ ...v, [key]: value }));

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const found = validateEmployee(values);
    setErrors(found);
    if (Object.keys(found).length > 0) return;
    setSaving(true);
    setServerError(undefined);
    try {
      if (editing) await api.updateEmployee(editing.id, values);
      else await api.createEmployee(values);
      onSaved(editing ? "Employee updated" : "Employee added");
    } catch (err) {
      setServerError((err as Error).message);
    } finally {
      setSaving(false);
    }
  }

  const text = (key: "full_name" | "email" | "job_title" | "department", label: string, type = "text") => (
    <div className="space-y-1">
      <Label htmlFor={key}>{label}</Label>
      <Input id={key} type={type} value={values[key]} aria-invalid={!!errors[key]} onChange={(e) => set(key, e.target.value)} />
      {errors[key] && <p className="text-xs text-destructive">{errors[key]}</p>}
    </div>
  );

  return (
    <form onSubmit={submit} noValidate className="space-y-4">
      <DialogHeader>
        <DialogTitle>{editing ? "Edit employee" : "Add employee"}</DialogTitle>
        <DialogDescription>Salary is the annual amount in the country&apos;s currency.</DialogDescription>
      </DialogHeader>
      {text("full_name", "Full name")}
      {text("email", "Email", "email")}
      <div className="grid grid-cols-2 gap-3">
        {text("job_title", "Job title")}
        {text("department", "Department")}
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1">
          <Label>Country</Label>
          <FilterSelect ariaLabel="Country" className="w-full" value={values.country} onChange={(v) => set("country", v)}
            allLabel="Select country" options={countries.map((c) => ({ value: c.code, label: `${c.name} (${c.currency})` }))} />
          {errors.country && <p className="text-xs text-destructive">{errors.country}</p>}
        </div>
        <div className="space-y-1">
          <Label htmlFor="salary">Annual salary</Label>
          <Input id="salary" type="number" min={1} value={values.salary || ""} aria-invalid={!!errors.salary}
            onChange={(e) => set("salary", e.target.value === "" ? 0 : Number(e.target.value))} />
          {errors.salary && <p className="text-xs text-destructive">{errors.salary}</p>}
        </div>
      </div>
      <div className="space-y-1">
        <Label htmlFor="hire_date">Hire date</Label>
        <Input id="hire_date" type="date" value={values.hire_date} aria-invalid={!!errors.hire_date} onChange={(e) => set("hire_date", e.target.value)} />
        {errors.hire_date && <p className="text-xs text-destructive">{errors.hire_date}</p>}
      </div>
      {serverError && <p role="alert" className="text-sm text-destructive">{serverError}</p>}
      <DialogFooter>
        <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
        <Button type="submit" disabled={saving}>{saving ? "Saving…" : "Save"}</Button>
      </DialogFooter>
    </form>
  );
}
