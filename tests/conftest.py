import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash
from app.db.base import Base
from app.db.session import engine
from app.main import app
from app.models.user import User

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    """Give a session to the test, and roll back after the test finishes."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client():
    """
    Create an instanc of the TestClient for FastAPI that can be used
    in the test to simulate HTTP requests.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def test_user(db_session):
    """Create an user for testing in the DB and return it."""

    user = User(
        email="test@example.com",
        username="testuser",
        password=get_password_hash("password123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def user_token_headers(test_user):
    """Create a JWT token for the test user and return the headers."""
    token = create_access_token(subject=test_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def create_transaction_factory(client, user_token_headers):
    """Factory fixture to create transaction for testing."""

    def _make_transaction(amount: float = 100.0, category: str = "General"):
        payload = {
            "amount": amount,
            "category": category,
            "description": f"Test transaction from category{category}",
        }
        response = client.post(
            "/api/v1/transactions/", json=payload, headers=user_token_headers
        )
        return response.json()

    return _make_transaction
