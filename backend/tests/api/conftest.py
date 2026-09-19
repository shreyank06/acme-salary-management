import pytest
from fastapi.testclient import TestClient

from app.database import init_db, make_engine, make_session_factory
from app.main import create_app


@pytest.fixture
def client() -> TestClient:
    engine = make_engine("sqlite://")
    init_db(engine)
    return TestClient(create_app(make_session_factory(engine)))


def new_employee(**overrides) -> dict:
    data = {
        "full_name": "Asha Rao",
        "email": "asha@acme.com",
        "job_title": "Engineer",
        "department": "Engineering",
        "country": "IN",
        "salary": 2_000_000,
        "hire_date": "2022-01-01",
    }
    data.update(overrides)
    return data
