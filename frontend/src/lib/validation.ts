import type { EmployeeInput } from "./types";

export type FormErrors = Partial<Record<keyof EmployeeInput, string>>;

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/** Client-side mirror of the API rules, for instant feedback. The server stays the authority. */
export function validateEmployee(v: EmployeeInput): FormErrors {
  const errors: FormErrors = {};
  if (!v.full_name.trim()) errors.full_name = "Name is required";
  if (!EMAIL_RE.test(v.email.trim())) errors.email = "Enter a valid email";
  if (!v.job_title.trim()) errors.job_title = "Job title is required";
  if (!v.department.trim()) errors.department = "Department is required";
  if (!v.country) errors.country = "Select a country";
  if (!Number.isInteger(v.salary) || v.salary <= 0) errors.salary = "Enter a positive whole number";
  if (!v.hire_date) errors.hire_date = "Hire date is required";
  return errors;
}
