from app.repositories.employee_repository import EmployeeFilters, EmployeeRepository
from tests.conftest import make_employee


def seed(repo: EmployeeRepository):
    rows = [
        make_employee(full_name="Asha Rao", email="asha@x.test", salary=2_000_000),
        make_employee(
            full_name="Bob Stone", email="bob@x.test", country="US", currency="USD",
            department="Sales", job_title="Account Executive", salary=90_000,
        ),
        make_employee(
            full_name="Carla Diaz", email="carla@x.test", country="US", currency="USD",
            salary=150_000,
        ),
    ]
    for r in rows:
        repo.add(r)


def test_add_and_get(session):
    repo = EmployeeRepository(session)
    e = repo.add(make_employee())
    assert e.id is not None
    assert repo.get(e.id).email == "asha@acme.test"
    assert repo.get_by_email("asha@acme.test").id == e.id
    assert repo.get(999) is None


def test_delete(session):
    repo = EmployeeRepository(session)
    e = repo.add(make_employee())
    repo.delete(e)
    assert repo.get(e.id) is None


def test_search_filters_by_country_and_department(session):
    repo = EmployeeRepository(session)
    seed(repo)
    items, total = repo.search(EmployeeFilters(country="US", department="Engineering"))
    assert total == 1 and items[0].full_name == "Carla Diaz"


def test_search_text_matches_name_or_email_case_insensitively(session):
    repo = EmployeeRepository(session)
    seed(repo)
    assert repo.search(EmployeeFilters(q="BOB"))[1] == 1
    assert repo.search(EmployeeFilters(q="carla@x"))[1] == 1


def test_search_salary_range_is_inclusive(session):
    repo = EmployeeRepository(session)
    seed(repo)
    _, total = repo.search(EmployeeFilters(min_salary=90_000, max_salary=150_000))
    assert total == 2


def test_search_sorting_and_pagination_report_full_total(session):
    repo = EmployeeRepository(session)
    seed(repo)
    items, total = repo.search(
        EmployeeFilters(), sort_by="salary", descending=True, offset=1, limit=1
    )
    assert total == 3
    assert [i.full_name for i in items] == ["Carla Diaz"]


def test_salary_rows_respects_filters(session):
    repo = EmployeeRepository(session)
    seed(repo)
    rows = repo.salary_rows(EmployeeFilters(country="US"))
    assert sorted(r.salary for r in rows) == [90_000, 150_000]


def test_facets_are_distinct_and_sorted(session):
    repo = EmployeeRepository(session)
    seed(repo)
    f = repo.facets()
    assert f["countries"] == ["IN", "US"]
    assert f["departments"] == ["Engineering", "Sales"]
