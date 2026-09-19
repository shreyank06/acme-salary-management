from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SALARY_", env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./salary.db"
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
