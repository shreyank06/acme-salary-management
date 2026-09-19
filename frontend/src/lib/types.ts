export interface Employee {
  id: number;
  full_name: string;
  email: string;
  job_title: string;
  department: string;
  country: string;
  currency: string;
  salary: number;
  hire_date: string;
}

export type EmployeeInput = Omit<Employee, "id" | "currency">;

export interface EmployeePage {
  items: Employee[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface Stats {
  count: number;
  total: number;
  min: number;
  max: number;
  avg: number;
  median: number;
}

export interface Summary {
  currency: string;
  headcount: number;
  countries: number;
  total_payroll: number;
  avg_salary: number;
  median_salary: number;
}

export interface BreakdownRow {
  key: string;
  currency: string;
  stats: Stats;
}

export interface Bucket {
  start: number;
  end: number;
  count: number;
}

export interface Distribution {
  currency: string;
  buckets: Bucket[];
}

export interface Facets {
  countries: string[];
  departments: string[];
  job_titles: string[];
}

export interface Country {
  code: string;
  name: string;
  currency: string;
}

export type GroupBy = "country" | "department" | "job_title";
export type SortField =
  | "full_name"
  | "job_title"
  | "department"
  | "country"
  | "salary"
  | "hire_date";

export interface EmployeeQuery {
  q?: string;
  country?: string;
  department?: string;
  job_title?: string;
  min_salary?: number;
  max_salary?: number;
  sort_by?: SortField;
  order?: "asc" | "desc";
  page?: number;
  page_size?: number;
}
