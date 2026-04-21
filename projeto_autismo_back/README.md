# projeto_autismo

Projeto de estudo FastAPI com estrutura modular inspirada em projeto de produção.

## Stack

- **FastAPI** — framework web async
- **SQLAlchemy 2 (async)** — ORM com suporte a asyncio
- **Alembic** — migrações de banco de dados
- **pydantic-settings** — configuração via `.env`
- **pwdlib[argon2]** — hash de senhas
- **PyJWT** — tokens JWT
- **uv** — gerenciador de pacotes e ambiente virtual

## Estrutura

```
projeto_autismo/
├── app/
│   ├── core/
│   │   └── settings.py        # Configurações centralizadas
│   ├── domains/
│   │   ├── auth/              # Autenticação (login, refresh token)
│   │   └── users/             # CRUD de usuários
│   ├── shared/
│   │   ├── db/                # Engine, sessão, registry e models
│   │   ├── errors.py          # HTTPExceptions compartilhadas
│   │   ├── schemas.py         # Schemas base (Message, HealthResponse, FilterPage)
│   │   └── security.py        # JWT e hash de senhas
│   ├── dependencies.py        # Aliases de Depends reutilizáveis
│   └── main.py                # Ponto de entrada (FastAPI app)
├── migrations/                # Alembic
├── tests/
│   ├── unit/                  # Testes sem I/O externo
│   └── integration/           # Testes com banco SQLite in-memory
├── .env                       # Variáveis locais (não commitar)
├── .env.example               # Template de variáveis
├── alembic.ini
├── pyproject.toml
└── pytest.ini
```

## Instalação

```bash
# Instalar uv (se ainda não tiver)
curl -Ls https://astral.sh/uv/install.sh | sh

# Criar ambiente e instalar dependências
uv sync --dev

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env conforme necessário
```

## Comandos

```bash
# Rodar o servidor em modo dev
uv run task run

# Rodar testes
uv run task test

# Rodar todos os testes com cobertura
uv run task test_all

# Lint e formatação
uv run task lint
uv run task format

# Aplicar migrações
uv run alembic upgrade head

# Gerar nova migração
uv run alembic revision --autogenerate -m "descricao"
```
