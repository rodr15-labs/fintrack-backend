import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.main import app

TEST_DATABASE_URL = "postgresql://admin:fintrack_db_psw@localhost:5432/fintrack_db"


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    """Give a session to the test, and roll back after the test finishes."""
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

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
