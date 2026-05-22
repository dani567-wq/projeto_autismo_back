from http import HTTPStatus
from fastapi import APIRouter
from app.dependencies import Session
from app.domains.contato.models import ContatoMessage
from app.domains.contato.schemas import ContatoCreate, ContatoPublic

router = APIRouter(prefix='/contato', tags=['contato'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ContatoPublic)
async def send_message(data: ContatoCreate, session: Session):
    msg = ContatoMessage(
        nome=data.nome,
        telefone=data.telefone,
        idade=data.idade,
        tipo=data.tipo,
        mensagem=data.mensagem,
    )
    session.add(msg)
    await session.commit()
    await session.refresh(msg)
    return msg
