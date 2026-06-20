# Guia Definitivo: `async def` vs `def` no FastAPI

Este guia serve como um lembrete rápido (cheat sheet) para quando usar funções assíncronas (`async def`) e síncronas (`def`) no seu projeto FastAPI.

## Regra de Ouro

* **Se você vai usar `await` dentro da função:** Use `async def`.
* **Se você NÃO vai usar `await` (ou está usando bibliotecas que não suportam assincronismo):** Use `def`.

---

## 1. Quando usar `async def` (Assíncrono)

Use `async def` quando a sua função realiza operações de **I/O-bound** (entrada e saída de rede/dados) usando bibliotecas que suportam assincronismo de forma nativa.

**Exemplos Clássicos:**
* Conexões com banco de dados usando drivers assíncronos (ex: `asyncpg` para Postgres, `Motor` para MongoDB, `aiosqlite` para SQLite).
* Chamadas de APIs externas usando clientes assíncronos (ex: `httpx.AsyncClient` ou `aiohttp`).
* Leitura/escrita de arquivos assíncrona (ex: `aiofiles`).

**Como o FastAPI lida com isso:**
O FastAPI executa essas funções diretamente no **Event Loop principal**. Quando a execução atinge um `await` (uma espera de rede, por exemplo), o FastAPI "pausa" essa requisição e vai atender outras requisições enquanto espera. É isso que dá ao FastAPI seu desempenho incrível para milhares de acessos.

**🚨 O Perigo:** 
NUNCA coloque código síncrono bloqueante (ex: queries demoradas do `psycopg2` tradicional, bibliotecas como `requests.get` ou processamentos muito longos) dentro de um `async def`. Como ele roda na thread principal, você vai travar o servidor inteiro até a tarefa terminar.

---

## 2. Quando usar `def` (Síncrono)

Use o `def` padrão quando você estiver usando bibliotecas tradicionais que **não** suportam `await`, ou quando for fazer processamentos pesados.

**Exemplos Clássicos:**
* Queries de banco de dados usando bibliotecas clássicas/síncronas (ex: `psycopg2` padrão, `sqlite3` nativo, SQLAlchemy na versão síncrona).
* Requisições HTTP usando a biblioteca comum `requests`.
* Processamento pesado de CPU (processamento de imagens, ML local, cálculos matemáticos intensos).

**Como o FastAPI lida com isso:**
Como o código síncrono "travaria" o Event Loop principal, o FastAPI percebe que você usou um `def` e inteligentemente joga a execução dessa rota para uma **Thread Pool externa**. Assim, a thread secundária fica bloqueada esperando o processamento, mas o Event Loop do FastAPI continua totalmente livre para atender novos usuários.

**✅ A Vantagem:**
Você pode usar qualquer código Python legado ou síncrono de forma segura sem medo de paralisar o seu servidor.

---

## Casos de Uso (Bancos de Dados)

### Se for usar PostgreSQL:
* **Caminho Moderno (Recomendado):** Usando bibliotecas como `asyncpg` ou `SQLAlchemy Async`.
  * **Rotas:** usar `async def`
  * **Serviços:** usar `async def`
* **Caminho Clássico:** Usando `psycopg2`.
  * **Rotas:** usar `def`
  * **Serviços:** usar `def`

### Se for usar SQLite:
* **Caminho Moderno (Recomendado):** Usando `aiosqlite` (lembre-se de ativar o modo WAL do SQLite).
  * **Rotas:** usar `async def`
  * **Serviços:** usar `async def`
* **Caminho Clássico:** Usando o módulo embutido do Python `sqlite3`.
  * **Rotas:** usar `def`
  * **Serviços:** usar `def`

---

## Tabela de Decisão Rápida

| Cenário / Ferramenta | O que usar | Por quê? |
| :--- | :--- | :--- |
| **Driver DB Async** (`asyncpg`, `aiosqlite`) | `async def` | Tem suporte a `await`. Roda no Event Loop com concorrência máxima. |
| **Driver DB Síncrono** (`psycopg2`, `sqlite3`) | `def` | Bloqueia a execução. O FastAPI te salva jogando para uma Thread separada. |
| **API Externa Async** (`httpx` assíncrono) | `async def` | Libera a fila enquanto espera a resposta de rede. |
| **API Externa Síncrona** (`requests.get`) | `def` | Trava a execução da rede, vai rodar em uma Thread externa. |
| **Algoritmo pesado** (Processamento puro CPU) | `def` | Ocupa toda a capacidade de processamento, precisa rodar fora do loop principal. |
| **Retornando dado rápido** da memória / cache | `async def` ou `def` | Tanto faz. Sendo muito rápido, não há grande impacto em usar `def`, mas `async def` corta o *overhead* da thread. |
