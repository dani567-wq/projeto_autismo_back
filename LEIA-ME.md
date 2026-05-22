# 🔵 Laço Azul — Projeto Autismo (com Backend Integrado)

## O que foi feito nesta versão

| Arquivo / Módulo | O que foi integrado |
|---|---|
| `autismo/login.html` | Conectado à API: login real com JWT + cadastro de conta |
| `autismo/jh.html` | Diário salvo na API (com fallback local); formulário de contato gravado no banco |
| `app/domains/diario/` | Novo módulo: endpoints `POST /diario/` e `GET /diario/` |
| `app/domains/contato/` | Novo módulo: endpoint `POST /contato/` |
| `app/main.py` | CORS liberado, novos routers incluídos, tabelas criadas automaticamente |
| `.env` | Configurado para SQLite local — funciona sem PostgreSQL |

---

## Como rodar localmente

### Pré-requisito
Ter o **Python 3.11+** instalado.

### Windows
Clique duas vezes em `iniciar_servidor.bat`

### Linux / Mac
```bash
./iniciar_servidor.sh
```

### Manual
```bash
pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite pyjwt "pwdlib[argon2]" python-multipart pydantic-settings email-validator
python -m uvicorn app.main:app --reload
```

---

## Usando o site

1. Inicie o servidor (acima)
2. Abra `autismo/login.html` no navegador
3. Crie uma conta → faça login → será redirecionado para `jh.html`
4. O **Diário** salva os registros no banco de dados
5. O **Formulário de Contato** envia a mensagem para o banco

## Rotas da API

| Método | Rota | Descrição | Auth? |
|---|---|---|---|
| `GET` | `/` | Health check | ❌ |
| `POST` | `/users/` | Criar conta | ❌ |
| `POST` | `/auth/token` | Login → JWT | ❌ |
| `POST` | `/diario/` | Salvar registro do diário | ✅ |
| `GET` | `/diario/` | Listar registros do usuário | ✅ |
| `POST` | `/contato/` | Enviar mensagem de contato | ❌ |

Documentação interativa: **http://localhost:8000/docs**

---

## Banco de dados

Arquivo gerado automaticamente: `database.db` (SQLite)

Para usar PostgreSQL, altere `DATABASE_URL` no `.env`:
```
DATABASE_URL=postgresql+asyncpg://user:senha@localhost:5432/projeto_autismo
```
