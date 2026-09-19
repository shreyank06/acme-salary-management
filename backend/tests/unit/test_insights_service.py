from app.repositories.employee_repository import EmployeeFilters, EmployeeRepository
from app.services.insights_service import InsightsService
from tests.conftest import make_employee


def build(session):
    repo = EmployeeRepository(session)
    for i, (country, cur, dept, salary) in enumerate(
        [
            ("US", "USD", "Engineering", 100_000),
            ("US", "USD", "Engineering", 200_000),
            ("US", "USD", "Sales", 60_000),
            ("IN", "INR", "Engineering", 2_500_000),  # = 30,000 USD
        ]
    ):
        repo.add(
            make_employee(
                email=f"e{i}@x.test",
                country=country,
                currency=cur,
                department=dept,
                salary=salary,
            )
        )
    return InsightsService(repo)


def test_summary_is_in_usd(session):
    s = build(session).summary(EmployeeFilters())
    assert s.currency == "USD"
    assert s.headcount == 4
    assert s.total_payroll == 100_000 + 200_000 + 60_000 + 30_000
    assert s.countries == 2


def test_by_country_uses_local_currency(session):
    rows = {r.key: r for r in build(session).breakdown("country")}
    assert rows["IN"].currency == "INR" and rows["IN"].stats.median == 2_500_000
    assert rows["US"].currency == "USD" and rows["US"].stats.median == 100_000


def test_by_department_without_country_is_usd_normalised(session):
    rows = {r.key: r for r in build(session).breakdown("department")}
    assert rows["Engineering"].currency == "USD"
    assert rows["Engineering"].stats.count == 3
    assert rows["Engineering"].stats.median == 100_000  # [30k, 100k, 200k]


def test_by_department_with_country_uses_local_currency(session):
    rows = {r.key: r for r in build(session).breakdown("department", country="IN")}
    assert set(rows) == {"Engineering"}
    assert rows["Engineering"].currency == "INR"
    assert rows["Engineering"].stats.max == 2_500_000


def test_breakdown_sorted_by_headcount_desc(session):
    rows = build(session).breakdown("department")
    assert [r.key for r in rows] == ["Engineering", "Sales"]


def test_distribution_counts_all_employees(session):
    dist = build(session).distribution(EmployeeFilters(), bucket_count=4)
    assert dist.currency == "USD"
    assert sum(b.count for b in dist.buckets) == 4
