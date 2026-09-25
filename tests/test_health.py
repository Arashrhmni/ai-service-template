from unittest.mock import AsyncMock, patch


async def test_health_all_ok(client):
    response = await client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["db"] == "ok"
    assert body["redis"] == "ok"


async def test_health_redis_down(client):
    with patch("app.routes.health.redis_client.ping", new=AsyncMock(side_effect=ConnectionError)):
        response = await client.get("/health")
        assert response.status_code == 503
        body = response.json()
        assert body["redis"].startswith("error")
        assert body["db"] == "ok"
