from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DB_USER: str = "admin"
    DB_PASSWORD: str = "fintrack_db_psw"
    DB_NAME: str = "fintrack_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
