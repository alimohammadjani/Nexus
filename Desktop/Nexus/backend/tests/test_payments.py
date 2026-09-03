"""Payment endpoint tests."""


def test_create_transaction(client, auth_headers):
    resp = client.post(
        "/api/v1/payments/transactions",
        json={"amount": 50, "currency": "USD", "description": "top up"},
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["status"] == "succeeded"
    assert body["reference"].startswith("devhub_")


def test_list_transactions(client, auth_headers):
    client.post("/api/v1/payments/transactions", json={"amount": 10}, headers=auth_headers)
    resp = client.get("/api/v1/payments/transactions", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


def test_get_transaction_owner(client, auth_headers):
    tx_id = client.post(
        "/api/v1/payments/transactions", json={"amount": 10}, headers=auth_headers
    ).json()["id"]
    resp = client.get(f"/api/v1/payments/transactions/{tx_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == tx_id


def test_get_transaction_not_found(client, auth_headers):
    resp = client.get("/api/v1/payments/transactions/99999", headers=auth_headers)
    assert resp.status_code == 404


def test_get_transaction_other_user_forbidden(client, auth_headers, register_user):
    tx_id = client.post(
        "/api/v1/payments/transactions", json={"amount": 10}, headers=auth_headers
    ).json()["id"]
    other = register_user("payer2@example.com")
    resp = client.get(f"/api/v1/payments/transactions/{tx_id}", headers=other)
    assert resp.status_code == 404


def test_get_transaction_admin_allowed(client, auth_headers, admin_headers):
    tx_id = client.post(
        "/api/v1/payments/transactions", json={"amount": 10}, headers=auth_headers
    ).json()["id"]
    resp = client.get(f"/api/v1/payments/transactions/{tx_id}", headers=admin_headers)
    assert resp.status_code == 200


def test_pay_transaction(client, auth_headers):
    tx_id = client.post(
        "/api/v1/payments/transactions", json={"amount": 10}, headers=auth_headers
    ).json()["id"]
    resp = client.post(f"/api/v1/payments/transactions/{tx_id}/pay", headers=auth_headers)
    assert resp.status_code == 201, resp.text
    assert resp.json()["transaction_id"] == tx_id


def test_pay_transaction_not_found(client, auth_headers):
    resp = client.post("/api/v1/payments/transactions/99999/pay", headers=auth_headers)
    assert resp.status_code == 404
