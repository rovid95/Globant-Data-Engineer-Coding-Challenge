from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_docs_accessible():
    response = client.get("/docs")
    assert response.status_code == 200

def test_sql_test_safe_query():
    response = client.post("/employees/sql-test/", json={"query": "SELECT 1"})
    assert response.status_code == 200
    assert "columns" in response.json()
    assert "rows" in response.json()

def test_hires_by_quarter_table():
    response = client.get("/employees/hires-by-quarter/")
    assert response.status_code == 200
    assert "<table" in response.text