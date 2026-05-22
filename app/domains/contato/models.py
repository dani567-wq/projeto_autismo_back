from datetime import datetime
from sqlalchemy import func, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.shared.db.registry import mapper_registry


@mapper_registry.mapped_as_dataclass
class ContatoMessage:
    __tablename__ = 'contato_messages'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    telefone: Mapped[str]
    idade: Mapped[str] = mapped_column(default='')
    tipo: Mapped[str] = mapped_column(default='')
    mensagem: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
