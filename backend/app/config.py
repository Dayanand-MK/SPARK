from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SPARK API"
    app_version: str = "0.1.0"
    environment: str = "development"

    database_url: str
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "scientific_papers"
    max_papers: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()