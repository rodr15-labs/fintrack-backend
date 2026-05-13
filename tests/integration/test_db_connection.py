from sqlalchemy import text


def test_db_connection_should_be_successful(db_session):
    result = db_session.execute(text("SELECT 1")).fetchone()
    assert result[0] == 1
