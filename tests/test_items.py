async def test_create_item(client):
    response = await client.post("/items", json={"name": "test item"})
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "test item"
    assert "id" in body
    assert "created_at" in body


async def test_get_item(client):
    create_response = await client.post("/items", json={"name": "fetchable item"})
    item_id = create_response.json()["id"]

    response = await client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "fetchable item"


async def test_get_item_not_found(client):
    response = await client.get("/items/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"