"""Extra marketplace endpoint tests (filters, auth, reviews)."""


def test_list_products_filters(client, auth_headers):
    client.post(
        "/api/v1/market/products",
        json={"title": "Fast Template", "description": "d", "price": 100, "category": "template"},
        headers=auth_headers,
    )
    client.post(
        "/api/v1/market/products",
        json={"title": "Cheap API", "description": "d", "price": 5, "category": "api"},
        headers=auth_headers,
    )
    by_cat = client.get("/api/v1/market/products?category=api").json()
    assert len(by_cat) == 1 and by_cat[0]["category"] == "api"
    by_search = client.get("/api/v1/market/products?search=Template").json()
    assert len(by_search) == 1
    by_min = client.get("/api/v1/market/products?min_price=50").json()
    assert all(p["price"] >= 50 for p in by_min)
    by_max = client.get("/api/v1/market/products?max_price=10").json()
    assert all(p["price"] <= 10 for p in by_max)


def test_get_product_404(client):
    resp = client.get("/api/v1/market/products/99999")
    assert resp.status_code == 404


def test_update_product_owner(client, auth_headers):
    pid = client.post(
        "/api/v1/market/products",
        json={"title": "P", "description": "d", "price": 10},
        headers=auth_headers,
    ).json()["id"]
    resp = client.put(f"/api/v1/market/products/{pid}", json={"title": "P2", "price": 20}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "P2"


def test_update_product_other_forbidden(client, auth_headers, register_user):
    pid = client.post(
        "/api/v1/market/products",
        json={"title": "P", "description": "d", "price": 10},
        headers=auth_headers,
    ).json()["id"]
    other = register_user("seller2@example.com")
    resp = client.put(f"/api/v1/market/products/{pid}", json={"title": "X"}, headers=other)
    assert resp.status_code == 403


def test_update_product_404(client, auth_headers):
    resp = client.put("/api/v1/market/products/99999", json={"title": "X"}, headers=auth_headers)
    assert resp.status_code == 404


def test_add_review_404(client, auth_headers):
    resp = client.post(
        "/api/v1/market/products/99999/reviews", json={"rating": 5}, headers=auth_headers
    )
    assert resp.status_code == 404


def test_create_order_404(client, auth_headers):
    resp = client.post(
        "/api/v1/market/orders", json={"product_id": 99999}, headers=auth_headers
    )
    assert resp.status_code == 404


def test_delete_product_owner(client, auth_headers):
    pid = client.post(
        "/api/v1/market/products",
        json={"title": "P", "description": "d", "price": 10},
        headers=auth_headers,
    ).json()["id"]
    resp = client.delete(f"/api/v1/market/products/{pid}", headers=auth_headers)
    assert resp.status_code == 204


def test_delete_product_other_forbidden(client, auth_headers, register_user):
    pid = client.post(
        "/api/v1/market/products",
        json={"title": "P", "description": "d", "price": 10},
        headers=auth_headers,
    ).json()["id"]
    other = register_user("seller3@example.com")
    resp = client.delete(f"/api/v1/market/products/{pid}", headers=other)
    assert resp.status_code == 403


def test_delete_product_404(client, auth_headers):
    resp = client.delete("/api/v1/market/products/99999", headers=auth_headers)
    assert resp.status_code == 404


def test_list_reviews(client, auth_headers):
    pid = client.post(
        "/api/v1/market/products",
        json={"title": "P", "description": "d", "price": 10},
        headers=auth_headers,
    ).json()["id"]
    client.post(
        f"/api/v1/market/products/{pid}/reviews",
        json={"rating": 4, "comment": "ok"},
        headers=auth_headers,
    )
    resp = client.get(f"/api/v1/market/products/{pid}/reviews")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
