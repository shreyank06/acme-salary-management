from datetime import date

import pytest
from sqlalchemy.orm import Session

from app.database import init_db, make_engine, make_session_factory
from app.models import Employee


@pytest.fixture
def session() -> Session:
    engine = make_engine("sqlite://")
    init_db(engine)
    with make_session_factory(engine)() as s:
        yield s


def make_employee(**overrides) -> Employee:
    data = dict(
        full_name="Asha Rao",
        email="asha@acme.test",
        job_title="Software Engineer",
        department="Engineering",
        country="IN",
        currency="INR",
        salary=2_000_000,
        hire_date=date(2022, 1, 15),
    )
    data.update(overrides)
    return Employee(**data)
