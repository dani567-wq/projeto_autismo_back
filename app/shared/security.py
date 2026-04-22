"""
Utilitários de segurança: criação de tokens JWT e autenticação de usuários.

Fluxo de autenticação:
  1. Login → create_access_token
  2. Toda rota protegida usa get_current_user como dependency
  3. get_current_user decodifica o JWT e busca o usuário no banco
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import Settings
from app.domains.users.models import User
from app.shared.db.database import get_session
from app.shared.errors import errors

settings = Settings()
pwd_context = PasswordHash.recommended()

# tokenUrl aponta para o endpoint que o Swagger usa para autenticar
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token', refreshUrl='auth/refresh_token'
)


# ── Criação de tokens JWT ────────────────────────────────────────────────── #


def create_access_token(data: dict) -> str:
    """
    Cria um JWT de curta duração para autenticação de requisições.

    O campo 'sub' (subject) deve conter o e-mail do usuário.
    Expiração definida por ACCESS_TOKEN_EXPIRE_MINUTES nas settings.
    """
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    return encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ── Hash de senhas ───────────────────────────────────────────────────────── #


def get_password_hash(password: str) -> str:
    """Retorna o hash Argon2 da senha em texto puro."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto puro corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)


# ── FastAPI Dependency: usuário autenticado ──────────────────────────────── #


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    FastAPI dependency que extrai e valida o JWT do header Authorization.

    Retorna o usuário autenticado ou lança 401 se:
    - O token for inválido ou malformado
    - O token estiver expirado
    - O usuário referenciado no token não existir no banco
    """
    credentials_exception = errors.INVALID_CREDENTIALS

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email: str | None = payload.get('sub')

        if not subject_email:
            raise credentials_exception

    except (DecodeError, ExpiredSignatureError):
        raise credentials_exception

    user = await session.scalar(
        select(User).where(User.email == subject_email)
    )

    if not user:
        raise credentials_exception

    return user
