"""
Configurações da aplicação carregadas via variáveis de ambiente / .env.

Em produção, defina as variáveis diretamente no ambiente (não use .env).
Em desenvolvimento, crie um arquivo .env na raiz do projeto
(veja .env.example para referência).
"""

from pathlib import Path
from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Localiza o .env na raiz do projeto independente de onde o processo roda.
# parents[2]: app/core/settings.py → app/core → app → projeto_autismo (raiz)
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / '.env'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        case_sensitive=True,
        env_file_encoding='utf-8',
        extra='ignore',
    )

    # ── Aplicação ──────────────────────────────────────────────────── #
    APP_NAME: str = 'projeto_autismo'
    ENVIRONMENT: str = 'development'  # 'development' | 'production'

    # ── Cookies ────────────────────────────────────────────────────── #

    @computed_field
    @property
    def COOKIE_SAME_SITE(self) -> Literal['lax', 'strict', 'none']:
        """
        Produção exige 'none' para cookies cross-origin.
        Desenvolvimento usa 'lax' para funcionar em HTTP.
        """
        if self.ENVIRONMENT == 'production':
            return 'none'
        return 'lax'

    @computed_field
    @property
    def COOKIE_SECURE(self) -> bool:
        """SameSite='none' exige Secure=True (apenas em produção)."""
        return self.ENVIRONMENT == 'production'

    # ── Autenticação JWT ───────────────────────────────────────────── #
    SECRET_KEY: str = 'test-secret-key-not-for-production'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ── Banco de dados ─────────────────────────────────────────────── #
    DB_USER: str = 'projeto_autismo'
    DB_PASSWORD: str = 'projeto_autismo'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_NAME: str = 'projeto_autismo'

    DATABASE_URL: str | None = None

    @computed_field
    @property
    def RESOLVED_DATABASE_URL(self) -> str:
        """
        Resolve a URL de conexão com o banco de dados.

        Prioriza DATABASE_URL do .env quando definida explicitamente.
        Caso contrário, monta dinamicamente com os campos DB_*.
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL

        return (
            f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )


settings = Settings()
