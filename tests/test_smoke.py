from app.core.testing import auth_headers, create_user


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_feature_router(client):
    data = create_user(client, email="smoke@example.com")
    res = client.get("/api/finlit/status", headers=auth_headers(data["token"]))
    assert res.status_code == 200
    assert res.json()["feature"] == "finlit"
