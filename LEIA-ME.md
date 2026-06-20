# 🔵 Laço Azul — Projeto Autismo (Frontend + Backend Integrados)

## O que foi feito nesta versão

| Arquivo / Módulo | O que foi integrado |
|---|---|
| `atismo_dois/index.html` | Página inicial reconstruída (tinha HTML duplicado/quebrado). Menu, botões e rodapé agora levam para os arquivos corretos do site. Formulário "Fale com especialista" conectado à API (`POST /contato/`) |
| `atismo_dois/oq-e-tea.html` | Antes era um fragmento sem cabeçalho/rodapé/CSS. Agora é uma página completa, com o mesmo menu e rodapé das outras páginas |
| `atismo_dois/login.html` | Conectado à API: login real com JWT + cadastro de conta. Corrigido bug que cancelava o login (havia um link `<a>` solto dentro do botão "Entrar"). Redirecionamento após login corrigido para `diario.html` |
| `atismo_dois/diario.html` | Diário salvo na API. Agora também carrega o nome real do usuário via `GET /users/me`. Botão de excluir registro agora funciona (endpoint criado no backend) |
| `app/domains/diario/` | Adicionado endpoint `DELETE /diario/{id}` (faltava — o frontend já chamava, mas o backend não tinha) |
| `app/domains/users/` | Adicionado endpoint `GET /users/me` (retorna os dados do usuário logado) |
| `app/domains/contato/` | Endpoint `POST /contato/` já existia; agora está de fato sendo usado pelo formulário da página inicial |
| `.env` | Configurado para SQLite local — funciona sem PostgreSQL |

---

## Navegação do site (como tudo se conecta)

```
index.html  (página inicial)
 ├─ "O que é TEA"        → oq-e-tea.html
 ├─ "Sinais / Direitos / Educadores / Adultos / Onde buscar ajuda / Contato"
 │                         → âncoras na própria index.html (#sinais, #direitos, ...)
 ├─ "Meu Diário"          → diario.html  (exige login)
 ├─ "Login"               → login.html
 └─ Formulário de contato → API: POST /contato/

oq-e-tea.html
 └─ Cabeçalho/rodapé levam de volta para index.html, diario.html e login.html

login.html
 ├─ Aba "Entrar"   → API: POST /auth/token  → salva o JWT → redireciona para diario.html
 └─ Aba "Criar conta" → API: POST /users/

diario.html  (exige token salvo no navegador)
 ├─ Carrega usuário → API: GET /users/me
 ├─ Lista registros → API: GET /diario/
 ├─ Salva registro  → API: POST /diario/
 ├─ Exclui registro → API: DELETE /diario/{id}
 └─ "Sair da conta" / "Início" → login.html / index.html
```

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

1. Inicie o servidor (acima) — ele fica em `http://localhost:8000`
2. Abra `atismo_dois/index.html` no navegador
3. Crie uma conta ou faça login em `login.html` → você será redirecionado para `diario.html`
4. O **Diário** salva, lista e exclui registros direto no banco de dados
5. O **Formulário de Contato** (na página inicial) envia a mensagem para o banco

> ⚠️ As páginas usam `http://localhost:8000` como endereço fixo da API (constante `API` / `API_BASE` no `<script>` de cada página). Se for hospedar a API em outro endereço, atualize essa constante em `index.html`, `login.html` e `diario.html`.

## Rotas da API

| Método | Rota | Descrição | Auth? |
|---|---|---|---|
| `GET` | `/` | Health check | ❌ |
| `POST` | `/users/` | Criar conta | ❌ |
| `GET` | `/users/me` | Dados do usuário logado | ✅ |
| `POST` | `/auth/token` | Login → JWT | ❌ |
| `POST` | `/auth/refresh_token` | Renovar token | ✅ |
| `POST` | `/diario/` | Salvar registro do diário | ✅ |
| `GET` | `/diario/` | Listar registros do usuário | ✅ |
| `DELETE` | `/diario/{id}` | Excluir um registro do diário | ✅ |
| `POST` | `/contato/` | Enviar mensagem de contato | ❌ |

Documentação interativa: **http://localhost:8000/docs**

---

## Banco de dados

Arquivo gerado automaticamente: `database.db` (SQLite)

Para usar PostgreSQL, altere `DATABASE_URL` no `.env`:
```
DATABASE_URL=postgresql+asyncpg://user:senha@localhost:5432/projeto_autismo
```

## Arquivos não usados pelo site

`atismo_dois/tb.html`, `atismo_dois/style.css` e `tb.js` (na raiz) parecem ser rascunhos de teste — nenhuma página do site os referencia. Podem ser apagados com segurança se não forem mais necessários.
