"""Seed the database with realistic, deterministic employee data.

python -m scripts.seed --count 10000 --seed 42 [--reset]
"""

import argparse
import random
from datetime import date, timedelta

from faker import Faker
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import init_db, make_engine, make_session_factory
from app.domain.countries import currency_for
from app.models import Employee

# (department, [(job title, base annual salary in USD)])
ROLES: dict[str, list[tuple[str, int]]] = {
    "Engineering": [
        ("Software Engineer", 95_000),
        ("Senior Software Engineer", 130_000),
        ("Staff Engineer", 175_000),
        ("QA Engineer", 75_000),
        ("DevOps Engineer", 105_000),
    ],
    "Data": [("Data Analyst", 80_000), ("Data Scientist", 120_000), ("ML Engineer", 140_000)],
    "Product": [("Product Manager", 125_000), ("Product Designer", 100_000)],
    "Sales": [("Sales Representative", 65_000), ("Account Executive", 90_000)],
    "Marketing": [("Marketing Specialist", 70_000), ("Content Strategist", 68_000)],
    "HR": [("HR Generalist", 65_000), ("Recruiter", 70_000), ("HR Manager", 95_000)],
    "Finance": [("Accountant", 72_000), ("Financial Analyst", 88_000)],
    "Operations": [("Operations Manager", 92_000), ("Support Specialist", 50_000)],
}
DEPT_WEIGHTS = [38, 10, 8, 14, 7, 4, 8, 11]

# Headcount weight and cost-of-labour multiplier relative to US pay.
COUNTRY_PROFILE: dict[str, tuple[int, float]] = {
    "US": (25, 1.00),
    "IN": (25, 0.30),
    "GB": (10, 0.80),
    "DE": (8, 0.85),
    "FR": (5, 0.75),
    "CA": (7, 0.85),
    "AU": (5, 0.90),
    "SG": (5, 0.90),
    "JP": (4, 0.75),
    "BR": (6, 0.35),
}
# 1 USD -> local currency, so a US-based base salary can be localised.
USD_TO_LOCAL = {
    "USD": 1,
    "GBP": 1 / 1.27,
    "INR": 1 / 0.012,
    "EUR": 1 / 1.08,
    "CAD": 1 / 0.74,
    "AUD": 1 / 0.66,
    "SGD": 1 / 0.74,
    "JPY": 1 / 0.0067,
    "BRL": 1 / 0.20,
}


def _round_salary(value: float, currency: str) -> int:
    step = 100_000 if currency == "INR" else 1_000 if currency == "JPY" else 500
    return max(step, int(round(value / step)) * step)


def generate_employees(count: int, seed: int = 42) -> list[Employee]:
    rng = random.Random(seed)
    fake = Faker()
    fake.seed_instance(seed)
    codes = list(COUNTRY_PROFILE)
    weights = [COUNTRY_PROFILE[c][0] for c in codes]
    departments = list(ROLES)
    today = date(2026, 1, 1)
    employees: list[Employee] = []
    for i in range(count):
        country = rng.choices(codes, weights)[0]
        currency = currency_for(country)
        department = rng.choices(departments, DEPT_WEIGHTS)[0]
        title, base_usd = rng.choice(ROLES[department])
        tenure_days = int(rng.triangular(30, 365 * 12, 365 * 2))
        # +-15% individual spread, +2%/year of tenure (capped)
        factor = rng.gauss(1.0, 0.08) * (1 + min(tenure_days / 365, 10) * 0.02)
        local = base_usd * COUNTRY_PROFILE[country][1] * factor * USD_TO_LOCAL[currency]
        name = fake.name()
        slug = "".join(ch for ch in name.lower() if ch.isalpha() or ch == " ").replace(" ", ".")
        employees.append(
            Employee(
                full_name=name,
                email=f"{slug}.{i}@acme-corp.com",  # index suffix guarantees uniqueness
                job_title=title,
                department=department,
                country=country,
                currency=currency,
                salary=_round_salary(local, currency),
                hire_date=today - timedelta(days=tenure_days),
            )
        )
    return employees


def seed_database(session: Session, count: int = 10_000, seed: int = 42) -> int:
    """Insert `count` employees if the table is empty. Returns number inserted."""
    if session.scalar(select(func.count(Employee.id))):
        return 0
    session.add_all(generate_employees(count, seed))
    session.commit()
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--reset", action="store_true", help="delete existing employees first")
    args = parser.parse_args()

    engine = make_engine(settings.database_url)
    init_db(engine)
    with make_session_factory(engine)() as session:
        if args.reset:
            session.execute(delete(Employee))
            session.commit()
        inserted = seed_database(session, args.count, args.seed)
    print(f"Inserted {inserted} employees" if inserted else "Database already seeded (use --reset)")


if __name__ == "__main__":
    main()
