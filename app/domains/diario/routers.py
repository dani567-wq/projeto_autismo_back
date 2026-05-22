from http import HTTPStatus
from fastapi import APIRouter
from sqlalchemy import select
from app.dependencies import CurrentUser, Session
from app.domains.diario.models import DiarioEntry
from app.domains.diario.schemas import DiarioEntryCreate, DiarioEntryPublic, DiarioList

router = APIRouter(prefix='/diario', tags=['diario'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=DiarioEntryPublic)
async def create_entry(entry: DiarioEntryCreate, session: Session, current_user: CurrentUser):
    db_entry = DiarioEntry(
        user_id=current_user.id,
        tipo=entry.tipo,
        data=entry.data,
        conteudo=entry.conteudo,
    )
    session.add(db_entry)
    await session.commit()
    await session.refresh(db_entry)
    return db_entry


@router.get('/', response_model=DiarioList)
async def list_entries(session: Session, current_user: CurrentUser):
    result = await session.scalars(
        select(DiarioEntry)
        .where(DiarioEntry.user_id == current_user.id)
        .order_by(DiarioEntry.data.desc())
    )
    return {'entries': result.all()}
