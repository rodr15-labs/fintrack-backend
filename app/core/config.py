import os

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = ".env.test" if os.getenv("TESTING") == "true" else ".env"


class Settings(BaseSettings):
    TESTING: bool = False
    DB_USER: str = "admin"
    DB_PASSWORD: str = "fintrack_db_psw"
    DB_NAME: str = "fintrack_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    SECRET_KEY: str = "dev-secret-key"
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def database_name(self) -> str:
        if self.TESTING:
            return f"{self.DB_NAME}_test"

        return self.DB_NAME

    @property
    def database_port(self) -> int:
        if self.TESTING:
            return 5433

        return self.DB_PORT

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://"
            f"{self.DB_USER}:"
            f"{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:"
            f"{self.database_port}/"
            f"{self.database_name}"
        )

    model_config = SettingsConfigDict(
        extra="ignore",
    )


settings = Settings(_env_file=ENV_FILE)
