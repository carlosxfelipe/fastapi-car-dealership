#!/bin/bash
echo "======================================"
echo "--- Benchmark: FastAPI (Local) ---"
echo "======================================"

# Garante que a porta 8000 está livre
fuser -k 8000/tcp 2>/dev/null || true

# Inicia o servidor em background
echo "Iniciando servidor FastAPI com uvloop..."
uv run uvicorn app.main:app --port 8000 --loop uvloop --workers 4 --log-level warning &
PID=$!

echo "Aguardando inicialização do servidor (5s)..."
sleep 5

echo "Iniciando teste de carga com autocannon (10 segundos, 100 conexões)..."
npx -y autocannon -c 100 -d 10 http://localhost:8000/cars

# Limpeza e finalização
echo "Limpando processos..."
kill -9 $PID 2>/dev/null || true
fuser -k 8000/tcp 2>/dev/null || true
echo "Benchmark Local Concluído!"
