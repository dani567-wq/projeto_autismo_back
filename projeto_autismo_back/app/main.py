"""
Ponto de entrada da aplicação FastAPI — projeto_autismo.

Documentação (Swagger / ReDoc):
  Desabilitada em produção — endpoints /docs e /redoc não são expostos.
  Em desenvolvimento, ficam ativos normalmente.
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
from app.shared.db.database import get_session
from app.shared.schemas import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Executado na inicialização (antes do yield) e no encerramento (após).
    """
    yield


# Docs desabilitadas em produção
_docs_url = '/docs' if settings.ENVIRONMENT != 'production' else None
_redoc_url = '/redoc' if settings.ENVIRONMENT != 'production' else None

app = FastAPI(
    title='projeto_autismo',
    lifespan=lifespan,
    redirect_slashes=False,
    docs_url=_docs_url,
    redoc_url=_redoc_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:5173',
        'http://127.0.0.1:5173',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_routers.router)
app.include_router(users_routers.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=HealthResponse)
async def read_root():
    """
    Health check — retorna status da API, ambiente e conectividade com o banco.
    """
    db_status = 'offline'
    db_url_display = settings.RESOLVED_DATABASE_URL

    try:
        async for session in get_session():
            await session.execute(text('SELECT 1'))
        db_status = 'online'
    except Exception:
        pass

    if settings.ENVIRONMENT == 'production':
        try:
            parsed = urlparse(db_url_display)
            db_url_display = parsed._replace(
                netloc=f'***:***@{parsed.hostname}:{parsed.port}'
            ).geturl()
        except Exception:
            db_url_display = '(oculto em produção)'

    return HealthResponse(
        message='Olá Mundo!',
        environment=settings.ENVIRONMENT,
        database_status=db_status,
        database_url=db_url_display,
    )
