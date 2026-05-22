"""
Utilitários de segurança: criação de tokens JWT e autenticação de usuários.
"""

from datetime import datetime, timedelta, timezone

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

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token', refreshUrl='auth/refresh_token'
)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    return encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> User:
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
