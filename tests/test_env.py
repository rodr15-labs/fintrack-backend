from app.core.config import Settings


def test_testing_environment_configuration():
    settings = Settings(_env_file=".env.test")

    assert settings.TESTING is True

    assert settings.DB_USER == "admin"
    assert settings.DB_PASSWORD == "fintrack_db_psw"

    assert settings.DB_HOST == "localhost"
    assert settings.database_port == 5433

    assert settings.database_name == "fintrack_db_test"

    assert settings.DATABASE_URL == (
        "postgresql://"
        "admin:"
        "fintrack_db_psw@"
        "localhost:"
        "5433/"
        "fintrack_db_test"
    )
