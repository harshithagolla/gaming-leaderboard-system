from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_submit_score():
    response = client.post(
        "/api/leaderboard/submit",
        json={
            "user_id": 1,
            "username": "alice",
            "score": 100
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == 1
    assert data["total_score"] == 100
    assert "rank" in data

def test_leaderboard_order():
    client.post("/api/leaderboard/submit", json={
        "user_id": 2,
        "username": "bob",
        "score": 200
    })

    response = client.get("/api/leaderboard/top?limit=2")
    assert response.status_code == 200

    data = response.json()["top"]

    assert len(data) == 2
    assert data[0]["user_id"] == 2  # highest score first
    assert data[1]["user_id"] == 1

def test_pagination():
    page1 = client.get("/api/leaderboard/top?limit=1&offset=0").json()
    page2 = client.get("/api/leaderboard/top?limit=1&offset=1").json()

    assert page1 != page2
