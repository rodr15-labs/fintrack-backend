def test_create_transaction(client, user_token_headers, test_user):
    transaction_data = {
        "amount": 100.0,
        "description": "Test Transaction",
        "category": "Test Category",
    }
    response = client.post(
        "/api/v1/transactions/", json=transaction_data, headers=user_token_headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["amount"] == transaction_data["amount"]
    assert data["description"] == transaction_data["description"]
    assert data["category"] == transaction_data["category"]
    assert data["user_id"] == test_user.id


def test_get_multiple_transactions(
    client, user_token_headers, create_transaction_factory
):
    transaction_count: int = 3
    for i in range(transaction_count):
        create_transaction_factory(amount=10.0 * (i + 1), category=f"Cat {i}")

    response = client.get("/api/v1/transactions/", headers=user_token_headers)

    assert response.status_code == 200
    assert len(response.json()) == transaction_count
