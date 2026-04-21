"""
Erros HTTP específicos do domínio de usuários.
Reexporta os erros compartilhados relevantes para conveniência.
"""

from app.shared.errors import errors  # noqa: F401

__all__ = ['errors']
