from http import HTTPStatus
from fastapi import APIRouter, HTTPException
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


@router.delete('/{entry_id}', status_code=HTTPStatus.OK)
async def delete_entry(entry_id: int, session: Session, current_user: CurrentUser):
    entry = await session.scalar(
        select(DiarioEntry).where(
            DiarioEntry.id == entry_id,
            DiarioEntry.user_id == current_user.id,
        )
    )

    if not entry:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Registro do diário não encontrado',
        )

    await session.delete(entry)
    await session.commit()

    return {'message': 'Registro excluído com sucesso'}
