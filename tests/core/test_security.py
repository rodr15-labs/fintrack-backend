import pytest
from jose import jwt

from app.core.config import settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)


@pytest.fixture
def password():
    return "supersecret"


@pytest.fixture
def hashed_password(password):
    return get_password_hash(password)


def test_password_hash(password, hashed_password):
    assert hashed_password != password
    assert isinstance(hashed_password, str)


def test_verify_password_success(password, hashed_password):
    assert verify_password(password, hashed_password) is True


def test_verify_password_fail(hashed_password):
    assert verify_password("wrongpassword", hashed_password) is False


def test_create_access_token():
    subject = "123"

    token = create_access_token(subject)

    decoded = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    assert decoded["sub"] == subject
    assert "exp" in decoded
