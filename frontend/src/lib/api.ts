import type {
  BreakdownRow,
  Country,
  Distribution,
  Employee,
  EmployeeInput,
  EmployeePage,
  EmployeeQuery,
  Facets,
  GroupBy,
  Summary,
} from "./types";

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

/** Serialise params, dropping undefined / null / empty-string values. */
export function buildQuery(params: object): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === null || value === "") continue;
    search.set(key, String(value));
  }
  const qs = search.toString();
  return qs ? `?${qs}` : "";
}

/** FastAPI returns `detail` as a string (domain errors) or a list (validation errors). */
export function extractErrorMessage(body: unknown, fallback: string): string {
  const detail = (body as { detail?: unknown } | null)?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail) && detail.length > 0) {
    const first = detail[0] as { loc?: unknown[]; msg?: string };
    const field = first.loc?.at(-1);
    return field ? `${String(field)}: ${first.msg}` : (first.msg ?? fallback);
  }
  return fallback;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${API_URL}${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", ...init?.headers },
    });
  } catch {
    throw new ApiError(0, "Cannot reach the server. Is the API running?");
  }
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new ApiError(res.status, extractErrorMessage(body, `Request failed (${res.status})`));
  }
  return res.status === 204 ? (undefined as T) : ((await res.json()) as T);
}

export const api = {
  listEmployees: (q: EmployeeQuery) =>
    request<EmployeePage>(`/api/employees${buildQuery(q)}`),
  createEmployee: (data: EmployeeInput) =>
    request<Employee>("/api/employees", { method: "POST", body: JSON.stringify(data) }),
  updateEmployee: (id: number, data: Partial<EmployeeInput>) =>
    request<Employee>(`/api/employees/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  deleteEmployee: (id: number) => request<void>(`/api/employees/${id}`, { method: "DELETE" }),
  facets: () => request<Facets>("/api/employees/facets"),
  countries: () => request<Country[]>("/api/countries"),
  summary: (p: { country?: string; department?: string } = {}) =>
    request<Summary>(`/api/insights/summary${buildQuery(p)}`),
  breakdown: (groupBy: GroupBy, country?: string) =>
    request<BreakdownRow[]>(`/api/insights/breakdown${buildQuery({ group_by: groupBy, country })}`),
  distribution: (p: { country?: string; department?: string } = {}) =>
    request<Distribution>(`/api/insights/distribution${buildQuery(p)}`),
};
