from tests.api.conftest import new_employee


def seed(client):
    for i, (country, salary) in enumerate([("US", 100_000), ("US", 200_000), ("IN", 2_500_000)]):
        client.post(
            "/api/employees",
            json=new_employee(email=f"e{i}@acme.com", country=country, salary=salary),
        )


def test_summary(client):
    seed(client)
    body = client.get("/api/insights/summary").json()
    assert body["headcount"] == 3 and body["currency"] == "USD"
    assert body["total_payroll"] == 330_000


def test_breakdown_by_country(client):
    seed(client)
    rows = {r["key"]: r for r in client.get("/api/insights/breakdown").json()}
    assert rows["US"]["stats"]["median"] == 150_000 and rows["IN"]["currency"] == "INR"


def test_breakdown_rejects_unknown_group(client):
    assert client.get("/api/insights/breakdown", params={"group_by": "salary"}).status_code == 422


def test_distribution(client):
    seed(client)
    body = client.get("/api/insights/distribution", params={"buckets": 3}).json()
    assert sum(b["count"] for b in body["buckets"]) == 3


def test_countries_catalogue(client):
    assert any(c["code"] == "IN" for c in client.get("/api/countries").json())
