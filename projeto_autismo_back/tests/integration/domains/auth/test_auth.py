"""
Testes de integração do domínio de autenticação.
Cobrem login, refresh de token e casos de erro.
"""

from http import HTTPStatus

import pytest
from freezegun import freeze_time


@pytest.mark.integration
def test_login_retorna_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'bearer'


@pytest.mark.integration
def test_login_usuario_inexistente_retorna_401(client):
    response = client.post(
        '/auth/token',
        data={'username': 'naoexiste@dominio.com', 'password': 'qualquer'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.integration
def test_login_senha_errada_retorna_401(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'senha_errada'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.integration
def test_refresh_token_retorna_novo_token(client, user, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


@pytest.mark.integration
def test_token_expirado_retorna_401(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'qualquer',
                'email': 'qualquer@teste.com',
                'password': 'qualquer',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.integration
def test_token_expirado_nao_renova(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
