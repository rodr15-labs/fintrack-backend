import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_access_token, get_password_hash
from app.db.base import Base
from app.main import app
from app.models.user import User

engine = create_engine(settings.DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    """Crea las tablas una sola vez para toda la sesión de tests."""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Crea una sesión de base de datos aislada para cada test.
    Todo lo que ocurra aquí se revierte al finalizar el test.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    Creates a TestClient that forces the app to use the same db session as the test.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session):
    """
    Create a test user in the db and return it
    """
    user = User(
        email="test@example.com",
        username="testuser",
        password=get_password_hash("password123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def user_token_headers(test_user):
    """Creates the auth headers with a valid JWT token for the test user."""
    token = create_access_token(subject=str(test_user.id))
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def create_transaction_factory(client, user_token_headers):
    """Factory for creating transactions via API."""

    def _make_transaction(amount: float = 100.0, category: str = "General"):
        payload = {
            "amount": amount,
            "category": category,
            "description": f"Test transaction from category {category}",
        }
        response = client.post(
            "/api/v1/transactions/", json=payload, headers=user_token_headers
        )
        return response.json()

    return _make_transaction
