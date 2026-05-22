"""
Ponto de entrada da aplicação FastAPI — projeto_autismo.
"""

from contextlib import asynccontextmanager
from http import HTTPStatus
from urllib.parse import urlparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.settings import settings
from app.domains.auth import routers as auth_routers
from app.domains.users import routers as users_routers
from app.domains.diario import routers as diario_routers
from app.domains.contato import routers as contato_routers
from app.shared.db.database import get_session, engine
from app.shared.db.registry import mapper_registry
from app.shared.schemas import HealthResponse

# Import models so they are registered
import app.domains.users.models  # noqa
import app.domains.diario.models  # noqa
import app.domains.contato.models  # noqa


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-create all tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
    yield


_docs_url = '/docs' if settings.ENVIRONMENT != 'production' else None
_redoc_url = '/redoc' if settings.ENVIRONMENT != 'production' else None

app = FastAPI(
    title='Laço Azul — Projeto Autismo',
    lifespan=lifespan,
    redirect_slashes=False,
    docs_url=_docs_url,
    redoc_url=_redoc_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_routers.router)
app.include_router(users_routers.router)
app.include_router(diario_routers.router)
app.include_router(contato_routers.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=HealthResponse)
async def read_root():
    db_status = 'offline'
    db_url_display = settings.RESOLVED_DATABASE_URL

    try:
        async for session in get_session():
            await session.execute(text('SELECT 1'))
        db_status = 'online'
    except Exception:
        pass

    return HealthResponse(
        message='Olá Mundo! API Laço Azul ativa.',
        environment=settings.ENVIRONMENT,
        database_status=db_status,
        database_url=db_url_display,
    )
