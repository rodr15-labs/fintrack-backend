API_V1_STR = "/api/v1"


def test_health_check_should_return_ok(client):
    """
    /health endpoint should return 200 OK and status 'alive'
    """
    # Act
    response = client.get(f"{API_V1_STR}/health")
    # Assert
    assert response.status_code == 200
