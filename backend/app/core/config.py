from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    embedding_dim: int = 768
    secret_key: str  # generar una clave larga y random, NUNCA hardcodear
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 1 día
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",extra="ignore")
    ADMIN_DNI: str | None = None
    ADMIN_PASSWORD: str | None = None
    ADMIN_NOMBRES: str = "Paola Cristina"
    ADMIN_APELLIDOS: str = "Marroquin Pinto"

settings = Settings()