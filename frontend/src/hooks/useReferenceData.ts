import { api } from "@/lib/api";
import type { Country, Facets } from "@/lib/types";
import { useAsync } from "./useAsync";

/** Countries + distinct departments/titles used to populate selects. */
export function useReferenceData(): {
  countries: Country[];
  facets: Facets;
  countryName: (code: string) => string;
} {
  const countries = useAsync(() => api.countries(), []).data ?? [];
  const facets = useAsync(() => api.facets(), []).data ?? {
    countries: [],
    departments: [],
    job_titles: [],
  };
  const byCode = new Map(countries.map((c) => [c.code, c.name]));
  return { countries, facets, countryName: (code) => byCode.get(code) ?? code };
}
