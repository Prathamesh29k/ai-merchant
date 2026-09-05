import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parents[1] / "backend"))

from config import settings  # noqa: E402
from database import get_connection, init_db  # noqa: E402
from main import app  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_database(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "database_url", f"sqlite:///{tmp_path / 'test.db'}")
    monkeypatch.setattr(settings, "daily_limit_paise", 5000)
    init_db()
    with get_connection() as db:
        db.execute("INSERT INTO products (name, category, description, price_paise, stock) VALUES (?, ?, ?, ?, ?)",
                   ("Test Mouse", "mouse", "test", 3000, 10))
        db.commit()
    yield


def test_health_check():
    assert TestClient(app).get("/health").json()["status"] == "ok"


def test_product_listing():
    response = TestClient(app).get("/api/products")
    assert response.status_code == 200
    assert response.json()[0]["price_paise"] == 3000


def test_order_creation_within_limit():
    response = TestClient(app).post("/api/orders", json={"product_id": 1, "quantity": 1, "agent_id": "buyer-1"})
    assert response.status_code == 200
    assert response.json()["daily_total_paise"] == 3000


def test_daily_limit_exceeded_failure_case():
    client = TestClient(app)
    client.post("/api/orders", json={"product_id": 1, "quantity": 1, "agent_id": "buyer-2"})
    response = client.post("/api/orders", json={"product_id": 1, "quantity": 1, "agent_id": "buyer-2"})
    assert response.status_code == 400
    assert response.json()["detail"]["error_code"] == "daily_limit_exceeded"
    assert TestClient(app).get("/api/audit").json()[0]["decision"] == "rejected"