"""
Fábrica de HTTPExceptions compartilhadas entre domínios.

Uso:
    from app.shared.errors import errors

    raise errors.INSUFFICIENT_PERMISSIONS
    raise errors.INVALID_CREDENTIALS
"""

from http import HTTPStatus

from fastapi import HTTPException

# ── Catálogo de mensagens por idioma ─────────────────────────────────── #

_MESSAGES: dict[str, dict[str, str]] = {
    'pt-BR': {
        'INVALID_CREDENTIALS': 'Não foi possível validar as credenciais',
        'INSUFFICIENT_PERMISSIONS': 'Permissão insuficiente',
        'USER_NOT_FOUND': 'Usuário não encontrado',
        'USERNAME_TAKEN': 'Nome de usuário já existe',
        'EMAIL_TAKEN': 'E-mail já existe',
        'USERNAME_OR_EMAIL_TAKEN': 'Nome de usuário ou e-mail já existe',
        'INCORRECT_CREDENTIALS': 'E-mail ou senha incorretos',
    },
    'en': {
        'INVALID_CREDENTIALS': 'Could not validate credentials',
        'INSUFFICIENT_PERMISSIONS': 'Insufficient permissions',
        'USER_NOT_FOUND': 'User not found',
        'USERNAME_TAKEN': 'Username already exists',
        'EMAIL_TAKEN': 'Email already exists',
        'USERNAME_OR_EMAIL_TAKEN': 'Username or Email already exists',
        'INCORRECT_CREDENTIALS': 'Incorrect email or password',
    },
}

_DEFAULT_LOCALE = 'pt-BR'


def _msg(key: str, locale: str = _DEFAULT_LOCALE) -> str:
    catalog = _MESSAGES.get(locale) or _MESSAGES[_DEFAULT_LOCALE]
    return catalog.get(key) or _MESSAGES[_DEFAULT_LOCALE][key]


# ── Fábrica ──────────────────────────────────────────────────────────── #


class _SharedErrors:
    """
    Namespace de HTTPExceptions transversais a todos os domínios.

    Erros sem parâmetros dinâmicos são propriedades que retornam
    uma nova instância a cada acesso — necessário porque FastAPI
    pode modificar o objeto de exceção internamente.
    """

    # ── 401 Unauthorized ─────────────────────────────────────────── #

    @property
    def INVALID_CREDENTIALS(self) -> HTTPException:
        return HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=_msg('INVALID_CREDENTIALS'),
            headers={'WWW-Authenticate': 'Bearer'},
        )

    @property
    def INCORRECT_CREDENTIALS(self) -> HTTPException:
        return HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=_msg('INCORRECT_CREDENTIALS'),
        )

    # ── 403 Forbidden ────────────────────────────────────────────── #

    @property
    def INSUFFICIENT_PERMISSIONS(self) -> HTTPException:
        return HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=_msg('INSUFFICIENT_PERMISSIONS'),
        )

    # ── 404 Not Found ────────────────────────────────────────────── #

    @property
    def USER_NOT_FOUND(self) -> HTTPException:
        return HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=_msg('USER_NOT_FOUND'),
        )

    # ── 409 Conflict ─────────────────────────────────────────────── #

    @property
    def USERNAME_TAKEN(self) -> HTTPException:
        return HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=_msg('USERNAME_TAKEN'),
        )

    @property
    def EMAIL_TAKEN(self) -> HTTPException:
        return HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=_msg('EMAIL_TAKEN'),
        )

    @property
    def USERNAME_OR_EMAIL_TAKEN(self) -> HTTPException:
        return HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=_msg('USERNAME_OR_EMAIL_TAKEN'),
        )


errors = _SharedErrors()
