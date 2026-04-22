"""
Testes de integração do domínio de usuários.
Cobrem CRUD completo e casos de erro de autorização/conflito.
"""

from http import HTTPStatus

import pytest

from app.domains.users.schemas import UserPublic


@pytest.mark.integration
def test_criar_usuario(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


@pytest.mark.integration
def test_criar_usuario_username_duplicado_retorna_409(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'outro@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT


@pytest.mark.integration
def test_criar_usuario_email_duplicado_retorna_409(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'outro_username',
            'email': user.email,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT


@pytest.mark.integration
def test_listar_usuarios_vazio(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


@pytest.mark.integration
def test_listar_usuarios_com_usuario(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


@pytest.mark.integration
def test_atualizar_usuario(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'nova_senha',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


@pytest.mark.integration
def test_atualizar_usuario_conflito_retorna_409(client, user, token):
    # Cria segundo usuário
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Tenta renomear o user da fixture para o nome já existente
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'nova_senha',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT


@pytest.mark.integration
def test_atualizar_usuario_sem_permissao_retorna_403(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'nova_senha',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.integration
def test_deletar_usuario(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


@pytest.mark.integration
def test_deletar_usuario_sem_permissao_retorna_403(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
