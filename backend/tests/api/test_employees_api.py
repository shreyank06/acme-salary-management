from tests.api.conftest import new_employee


def test_create_returns_201_with_derived_currency(client):
    r = client.post("/api/employees", json=new_employee())
    assert r.status_code == 201
    assert r.json()["currency"] == "INR" and r.json()["id"]


def test_create_validation_error_is_422(client):
    r = client.post("/api/employees", json=new_employee(salary=-5, country="ZZ"))
    assert r.status_code == 422


def test_duplicate_email_is_409(client):
    client.post("/api/employees", json=new_employee())
    assert client.post("/api/employees", json=new_employee()).status_code == 409


def test_get_missing_is_404(client):
    assert client.get("/api/employees/42").status_code == 404


def test_patch_updates_partial_fields(client):
    eid = client.post("/api/employees", json=new_employee()).json()["id"]
    r = client.patch(f"/api/employees/{eid}", json={"salary": 3_000_000})
    assert r.status_code == 200 and r.json()["salary"] == 3_000_000


def test_delete_then_404(client):
    eid = client.post("/api/employees", json=new_employee()).json()["id"]
    assert client.delete(f"/api/employees/{eid}").status_code == 204
    assert client.get(f"/api/employees/{eid}").status_code == 404


def test_list_paginates_filters_and_sorts(client):
    for i in range(5):
        client.post(
            "/api/employees",
            json=new_employee(email=f"e{i}@acme.com", salary=100_000 + i, country="US"),
        )
    client.post("/api/employees", json=new_employee(email="in@acme.com"))
    r = client.get(
        "/api/employees",
        params={"country": "US", "sort_by": "salary", "order": "desc", "page_size": 2, "page": 2},
    ).json()
    assert r["total"] == 5 and r["pages"] == 3
    assert [e["salary"] for e in r["items"]] == [100_002, 100_001]


def test_list_rejects_bad_page_size(client):
    assert client.get("/api/employees", params={"page_size": 1000}).status_code == 422


def test_facets(client):
    client.post("/api/employees", json=new_employee())
    assert client.get("/api/employees/facets").json()["countries"] == ["IN"]


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}
