import os
from functools import lru_cache
from typing import List


DEFAULT_LOCAL_CORS_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]
DEFAULT_TOKEN_SECRET = "local-dev-garda-change-me"


class Settings:
    def __init__(self) -> None:
        self.app_env = os.getenv("APP_ENV", "local").strip().lower() or "local"
        self.database_url = (
            os.getenv("DATABASE_URL")
            or os.getenv("SUPABASE_DB_URL")
            or "postgresql://postgres:postgres@127.0.0.1:54322/postgres"
        )
        self.auth_token_secret = os.getenv("AUTH_TOKEN_SECRET", DEFAULT_TOKEN_SECRET)
        self.auth_token_ttl_seconds = int(os.getenv("AUTH_TOKEN_TTL_SECONDS", "43200"))
        self.cors_allow_origins = self._parse_cors_origins(os.getenv("CORS_ALLOW_ORIGINS", ""))

    @staticmethod
    def _parse_cors_origins(raw: str) -> List[str]:
        if not raw.strip():
            return list(DEFAULT_LOCAL_CORS_ORIGINS)
        return [item.strip() for item in raw.split(",") if item.strip()]

    @property
    def requires_strict_secrets(self) -> bool:
        return self.app_env in {"production", "staging"}


@lru_cache
def get_settings() -> Settings:
    return Settings()


def validate_runtime_settings() -> None:
    settings = get_settings()
    if settings.requires_strict_secrets and settings.auth_token_secret == DEFAULT_TOKEN_SECRET:
        raise RuntimeError("AUTH_TOKEN_SECRET must be overridden outside local/dev environments")
