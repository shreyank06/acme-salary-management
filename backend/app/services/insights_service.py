from collections import defaultdict
from dataclasses import dataclass
from typing import Literal

from app.domain.countries import to_usd
from app.domain.stats import Bucket, SalaryStats, histogram, median, summarize
from app.repositories.employee_repository import EmployeeFilters, EmployeeRepository, SalaryRow

GroupBy = Literal["country", "department", "job_title"]
BASE_CURRENCY = "USD"


@dataclass(frozen=True)
class Summary:
    currency: str
    headcount: int
    countries: int
    total_payroll: int
    avg_salary: float
    median_salary: float


@dataclass(frozen=True)
class BreakdownRow:
    key: str
    currency: str
    stats: SalaryStats


@dataclass(frozen=True)
class Distribution:
    currency: str
    buckets: list[Bucket]


class InsightsService:
    """Read-only analytics.

    Currency rule: figures are in local currency when the result is scoped to a single
    country (grouping by country, or an explicit country filter); otherwise they are
    normalised to USD with the static FX table so cross-country numbers are comparable.
    """

    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    def summary(self, filters: EmployeeFilters) -> Summary:
        rows = self.repo.salary_rows(filters)
        values = [to_usd(r.salary, r.currency) for r in rows]
        if not values:
            return Summary(BASE_CURRENCY, 0, 0, 0, 0, 0)
        return Summary(
            currency=BASE_CURRENCY,
            headcount=len(values),
            countries=len({r.country for r in rows}),
            total_payroll=sum(values),
            avg_salary=round(sum(values) / len(values), 2),
            median_salary=median(values),
        )

    def breakdown(self, group_by: GroupBy, country: str | None = None) -> list[BreakdownRow]:
        rows = self.repo.salary_rows(EmployeeFilters(country=country))
        local = group_by == "country" or country is not None
        groups: dict[str, list[SalaryRow]] = defaultdict(list)
        for r in rows:
            groups[getattr(r, group_by)].append(r)
        result = [
            BreakdownRow(
                key=key,
                currency=members[0].currency if local else BASE_CURRENCY,
                stats=summarize([self._amount(m, local) for m in members]),
            )
            for key, members in groups.items()
        ]
        return sorted(result, key=lambda r: (-r.stats.count, r.key))

    def distribution(self, filters: EmployeeFilters, bucket_count: int = 10) -> Distribution:
        rows = self.repo.salary_rows(filters)
        local = filters.country is not None
        currency = rows[0].currency if (local and rows) else BASE_CURRENCY
        amounts = [self._amount(r, local) for r in rows]
        return Distribution(currency, histogram(amounts, bucket_count))

    @staticmethod
    def _amount(row: SalaryRow, local: bool) -> int:
        return row.salary if local else to_usd(row.salary, row.currency)
