from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse, ORJSONResponse

from app.cars_service import CarsService
from app.models import Car, CarCreate, CarCreateResponse

app = FastAPI(
    title="Oficial Car Dealership API",
    version="1.0.0",
    default_response_class=ORJSONResponse,
)


@app.get("/scalar", include_in_schema=False)
def scalar_docs():
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Oficial Car Dealership API - Scalar</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
        </head>
        <body>
            <script id="api-reference" data-url="/openapi.json"></script>
            <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
        </body>
        </html>
        """
    )


async def get_cars_service():
    return CarsService()


@app.get(
    "/cars",
    summary="Lista todos os carros",
    tags=["Carros"],
    description="Retorna a lista de carros em estoque.",
    response_model=List[Car],
)
async def get_cars(cars_service: CarsService = Depends(get_cars_service)):
    return cars_service.find_all()


@app.get(
    "/cars/{id}",
    summary="Pega um carro pelo ID",
    tags=["Carros"],
    description="Busca um carro específico pelo seu ID.",
    response_model=Car,
    responses={
        404: {"description": "Carro não encontrado"},
        422: {"description": "O ID fornecido não é um número válido"},
    },
)
async def get_car(id: int, cars_service: CarsService = Depends(get_cars_service)):
    car = await cars_service.find_one_by_id(id)
    if car:
        return car
    raise HTTPException(status_code=404, detail="Not found")


@app.post(
    "/cars",
    summary="Adiciona um carro",
    tags=["Carros"],
    description="Adiciona um novo carro ao estoque.",
    status_code=status.HTTP_201_CREATED,
    response_model=CarCreateResponse,
)
async def create_car(
    body: CarCreate, cars_service: CarsService = Depends(get_cars_service)
):
    car = await cars_service.create(body.brand, body.model)
    return {"status": f"Carro {car['brand']} adicionado com sucesso!", "car": car}
