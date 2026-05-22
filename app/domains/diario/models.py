from datetime import datetime
from sqlalchemy import func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.shared.db.registry import mapper_registry


@mapper_registry.mapped_as_dataclass
class DiarioEntry:
    __tablename__ = 'diario_entries'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    tipo: Mapped[str]           # 'crianca' | 'adulto'
    data: Mapped[str]           # ISO date string
    conteudo: Mapped[str] = mapped_column(Text)  # JSON serializado
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
