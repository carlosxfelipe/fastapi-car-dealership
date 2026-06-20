#!/bin/bash
echo "======================================"
echo "--- Benchmark: FastAPI (Local) ---"
echo "======================================"

kill_port() {
  local port=$1
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    lsof -ti tcp:${port} | xargs kill -9 2>/dev/null || true
  else
    # Linux
    fuser -k ${port}/tcp 2>/dev/null || true
  fi
}

# Garante que a porta 8000 está livre
kill_port 8000

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
kill_port 8000
echo "Benchmark Local Concluído!"
