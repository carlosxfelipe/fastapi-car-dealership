from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.cars_service import CarsService
from app.models import Car, CarCreate, CarCreateResponse
from app.responses import (
    create_car_responses,
    get_car_by_id_responses,
    list_cars_responses,
)

router = APIRouter(prefix="/cars", tags=["Carros"])

cars_service_instance = CarsService()


def get_cars_service():
    return cars_service_instance


CarsServiceDep = Annotated[CarsService, Depends(get_cars_service)]


@router.get(
    "",
    summary="Lista todos os carros",
    description="Retorna a lista de carros em estoque.",
    responses=list_cars_responses,
)
def find_all(cars_service: CarsServiceDep):
    return cars_service.find_all()


@router.get(
    "/{id}",
    summary="Pega um carro pelo ID",
    description="Busca um carro específico pelo seu ID.",
    response_model=Car,
    responses=get_car_by_id_responses,
)
def find_one_by_id(id: int, cars_service: CarsServiceDep):
    car = cars_service.find_one_by_id(id)
    if car:
        return car
    raise HTTPException(status_code=404, detail="Not found")


@router.post(
    "",
    summary="Adiciona um carro",
    description="Adiciona um novo carro ao estoque.",
    status_code=status.HTTP_201_CREATED,
    response_model=CarCreateResponse,
    responses=create_car_responses,
)
def create(body: CarCreate, cars_service: CarsServiceDep):
    car = cars_service.create(body.brand, body.model)
    return {"status": f"Carro {car['brand']} adicionado com sucesso!", "car": car}
