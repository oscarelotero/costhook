from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    PROJECT_NAME: str = "Costhook"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "postgresql+psycopg://localhost:5432/costhook"


settings = Settings()
