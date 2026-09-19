from sqlalchemy import func, select

from app.domain.countries import COUNTRIES, currency_for
from app.models import Employee
from scripts.seed import generate_employees, seed_database


def test_generation_is_deterministic():
    a = generate_employees(50, seed=1)
    b = generate_employees(50, seed=1)
    assert [(e.email, e.salary) for e in a] == [(e.email, e.salary) for e in b]


def test_emails_are_unique_and_currency_matches_country():
    employees = generate_employees(500, seed=7)
    assert len({e.email for e in employees}) == 500
    assert all(e.currency == currency_for(e.country) for e in employees)
    assert {e.country for e in employees} <= set(COUNTRIES)


def test_salaries_are_positive_ints():
    assert all(isinstance(e.salary, int) and e.salary > 0 for e in generate_employees(200, seed=3))


def test_seed_database_inserts_requested_count_and_is_idempotent(session):
    assert seed_database(session, count=120, seed=1) == 120
    assert seed_database(session, count=120, seed=1) == 0  # already populated
    assert session.scalar(select(func.count(Employee.id))) == 120
