#!/usr/bin/env python3
"""
Laço Azul — Script de inicialização do servidor
Instala dependências e sobe a API automaticamente.
"""
import subprocess, sys, os, webbrowser, time

DEPS = [
    "fastapi", "uvicorn[standard]", "sqlalchemy",
    "aiosqlite", "pyjwt", "pwdlib[argon2]",
    "python-multipart", "pydantic-settings", "email-validator"
]

print("=" * 50)
print("  Laço Azul — Servidor de Desenvolvimento")
print("=" * 50)

print("\n[1/2] Verificando dependências...")
subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "--quiet"] + DEPS,
    stdout=subprocess.DEVNULL
)
print("      OK")

print("[2/2] Iniciando API em http://localhost:8000")
print("\n  Documentação: http://localhost:8000/docs")
print("  Site:         abra atismo_dois/index.html no navegador")
print("\n  Pressione Ctrl+C para parar.\n")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

time.sleep(1)
try:
    subprocess.run(
        [sys.executable, "-m", "uvicorn", "app.main:app",
         "--host", "0.0.0.0", "--port", "8000", "--reload"]
    )
except KeyboardInterrupt:
    print("\nServidor encerrado.")
