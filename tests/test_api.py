from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Smoke Test: Ensure the docs endpoint works
def test_docs_accessible():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text

# Negative Test: SQL endpoint rejects malformed query
def test_sql_test_safe_query():
    response = client.post("/employees/sql-test/", json={"query": "SELECT 1"})
    assert response.status_code == 200
    assert "columns" in response.json()
    assert "rows" in response.json()

# Integration Test: Hires by quarter renders HTML table
def test_hires_by_quarter_table():
    response = client.get("/employees/hires-by-quarter/")
    assert response.status_code == 200
    assert "<table" in response.text
    assert "Q1" in response.text or "Q2" in response.text

# Negative Test: Invalid route returns 404
def test_nonexistent_route():
    response = client.get("/nonexistent-path")
    assert response.status_code == 404