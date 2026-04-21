"""Teste do endpoint raiz (health check)."""

from http import HTTPStatus

import pytest


@pytest.mark.integration
def test_root_retorna_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['message'] == 'Olá Mundo!'
    assert 'environment' in data
    assert 'database_status' in data
