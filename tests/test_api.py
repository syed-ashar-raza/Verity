from fastapi.testclient import TestClient

from verity.api import app


def test_health():
    r = TestClient(app).get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_evaluate_api():
    r = TestClient(app).post(
        "/v1/evaluate",
        json={
            "cases": [
                {
                    "id": "x",
                    "expected": "4",
                    "prediction": "4",
                    "metrics": {"exact_match": {"threshold": 1.0}},
                }
            ]
        },
    )
    assert r.status_code == 200 and r.json()["gate_passed"]
