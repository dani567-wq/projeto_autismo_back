"""
Testes unitários do módulo app.shared.security.

Não dependem de banco de dados — apenas lógica de criação e decodificação
de tokens JWT.
"""

import pytest
from http import HTTPStatus
from jwt import decode

from app.shared.security import create_access_token, settings


@pytest.mark.unit
def test_jwt_cria_token_valido():
    """create_access_token deve gerar um JWT decodificável com os dados corretos."""
    data = {'sub': 'usuario@teste.com'}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['sub'] == data['sub']
    assert 'exp' in decoded


@pytest.mark.unit
def test_jwt_token_invalido_retorna_401(client):
    """Token malformado deve resultar em 401."""
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert 'credenciais' in response.json()['detail'].lower() or \
           'credentials' in response.json()['detail'].lower()
