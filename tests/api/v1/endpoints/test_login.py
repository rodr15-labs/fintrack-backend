from app.core.errors import ErrorCode


def test_signup_user_success(client):
    """Test register a new user successfully."""
    payload = {
        "email": "test1@fintrack.com",
        "username": "tester1",
        "password": "strongpassword123",
    }
    response = client.post("/api/v1/login/signup", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
    assert "password" not in data


def test_signup_duplicate_email(client):
    """Test user cannot register with an email that already exists."""
    payload = {
        "email": "repetido@fintrack.com",
        "username": "user1",
        "password": "password123",
    }

    # Register the user for the first time
    client.post("/api/v1/login/signup", json=payload)

    # Register the user second time
    response = client.post("/api/v1/login/signup", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == ErrorCode.EMAIL_ALREADY_EXISTS


def test_login_success(client):
    """Registered user is able to login and recieve an access token."""

    # Register user
    email = "login_test@fintrack.com"
    password = "password123"
    client.post(
        "/api/v1/login/signup",
        json={"email": email, "username": "loginuser", "password": password},
    )

    # Try login
    login_data = {"username": email, "password": password}
    response = client.post("/api/v1/login/access-token", data=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Error when user tries to login with invalid credentials."""
    password = "wrongpassword"
    login_data = {"username": "noexiste@fintrack.com", "password": password}
    response = client.post("/api/v1/login/access-token", data=login_data)

    assert response.status_code == 400
    assert response.json()["detail"] == ErrorCode.INVALID_CREDENTIALS
