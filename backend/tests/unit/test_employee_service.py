from datetime import date

import pytest

from app.errors import ConflictError, NotFoundError
from app.repositories.employee_repository import EmployeeFilters, EmployeeRepository
from app.schemas import EmployeeCreate, EmployeeUpdate
from app.services.employee_service import EmployeeService


def payload(**overrides) -> EmployeeCreate:
    data = dict(
        full_name="Asha Rao", email="Asha@Acme.com", job_title="Engineer",
        department="Engineering", country="IN", salary=2_000_000, hire_date=date(2022, 1, 1),
    )
    data.update(overrides)
    return EmployeeCreate(**data)


@pytest.fixture
def service(session):
    return EmployeeService(EmployeeRepository(session))


def test_create_derives_currency_from_country_and_normalises_email(service):
    e = service.create(payload())
    assert e.currency == "INR"
    assert e.email == "asha@acme.com"


def test_create_rejects_duplicate_email(service):
    service.create(payload())
    with pytest.raises(ConflictError):
        service.create(payload(full_name="Someone Else"))


def test_schema_rejects_unsupported_country_and_non_positive_salary():
    with pytest.raises(ValueError):
        payload(country="ZZ")
    with pytest.raises(ValueError):
        payload(salary=0)


def test_get_missing_raises_not_found(service):
    with pytest.raises(NotFoundError):
        service.get(1)


def test_update_changes_only_provided_fields(service):
    e = service.create(payload())
    updated = service.update(e.id, EmployeeUpdate(salary=2_500_000))
    assert updated.salary == 2_500_000
    assert updated.full_name == "Asha Rao"


def test_update_country_re_derives_currency(service):
    e = service.create(payload())
    updated = service.update(e.id, EmployeeUpdate(country="US"))
    assert updated.currency == "USD"


def test_update_email_conflict_is_detected(service):
    service.create(payload())
    other = service.create(payload(email="b@acme.com"))
    with pytest.raises(ConflictError):
        service.update(other.id, EmployeeUpdate(email="asha@acme.com"))


def test_update_keeping_own_email_is_not_a_conflict(service):
    e = service.create(payload())
    service.update(e.id, EmployeeUpdate(email="asha@acme.com", salary=1))


def test_delete_then_get_raises(service):
    e = service.create(payload())
    service.delete(e.id)
    with pytest.raises(NotFoundError):
        service.get(e.id)


def test_list_returns_page_metadata(service):
    for i in range(5):
        service.create(payload(email=f"e{i}@acme.com"))
    page = service.list(
        EmployeeFilters(), sort_by="full_name", descending=False, page=2, page_size=2
    )
    assert page.total == 5 and page.page == 2 and len(page.items) == 2 and page.pages == 3
