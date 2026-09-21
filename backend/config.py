from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    SUPABASE_URL: str = Field(..., description="URL Supabase")
    SUPABASE_SERVICE_KEY: str = Field(..., description="Clé secrète service_role")
    SUPABASE_ANON_KEY: str = Field("", description="Clé anon")
    SUPABASE_JWT_SECRET: str = Field(..., description="Secret de signature JWT Supabase")
    DATABASE_URL: str = Field(..., description="URL de connexion asyncpg")

    OPENAI_API_KEY: str = Field(..., description="Clé OpenAI")
    ELEVENLABS_API_KEY: str = Field("", description="Clé ElevenLabs")
    ELEVENLABS_VOICE_ID: str = Field("21m00Tcm4TlvDq8ikWAM", description="ID Voix")

    TELEGRAM_BOT_TOKEN: str = Field("", description="Token bot Telegram")
    TELEGRAM_ALLOWED_USER_ID: int = Field(0, description="ID Telegram utilisateur autorisé")

    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
