"""Market endpoint tests."""


def test_list_products_empty(client):
    resp = client.get("/api/v1/market/products")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_product(client, auth_headers):
    payload = {"title": "Dashboard", "description": "Nice UI", "price": 100, "category": "template"}
    resp = client.post("/api/v1/market/products", json=payload, headers=auth_headers)
    assert resp.status_code == 201, resp.text
    assert resp.json()["title"] == "Dashboard"


def test_add_review_updates_rating(client, auth_headers):
    payload = {"title": "API", "description": "Fast API", "price": 50}
    product = client.post("/api/v1/market/products", json=payload, headers=auth_headers).json()
    review = client.post(
        f"/api/v1/market/products/{product['id']}/reviews",
        json={"rating": 5, "comment": "Great"},
        headers=auth_headers,
    )
    assert review.status_code == 201
    updated = client.get(f"/api/v1/market/products/{product['id']}").json()
    assert updated["rating"] == 5.0


def test_create_order(client, auth_headers):
    payload = {"title": "Plugin", "description": "Useful plugin", "price": 25}
    product = client.post("/api/v1/market/products", json=payload, headers=auth_headers).json()
    order = client.post(
        "/api/v1/market/orders", json={"product_id": product["id"]}, headers=auth_headers
    )
    assert order.status_code == 201
    assert order.json()["status"] == "paid"
