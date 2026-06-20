# Car Dealership API

## Setup

```bash
git clone https://github.com/carlosxfelipe/fastapi-car-dealership
cd fastapi-car-dealership
uv sync
uv run python scripts/dev.py
```

## Rotas

| Método | Rota        | Descrição              |
|--------|-------------|------------------------|
| GET    | /cars       | Lista todos os carros  |
| GET    | /cars/{id}  | Busca carro por ID     |
| POST   | /cars       | Adiciona um novo carro |

## Documentação

- Swagger: http://127.0.0.1:8000/docs
- Scalar: http://127.0.0.1:8000/scalar
