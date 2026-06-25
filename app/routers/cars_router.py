import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.cars_service import CarsService
from app.exceptions import CarNotFoundError
from app.models import Car, CarCreate, CarUpdate
from app.responses import (
    delete_car_responses,
    get_car_by_id_responses,
    update_car_responses,
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
    response_model=List[Car],
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
def find_one_by_id(id: uuid.UUID, cars_service: CarsServiceDep):
    try:
        return cars_service.find_one_by_id(id)
    except CarNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "",
    summary="Adiciona um carro",
    description="Adiciona um novo carro ao estoque.",
    status_code=status.HTTP_201_CREATED,
    response_model=Car,
)
def create(body: CarCreate, cars_service: CarsServiceDep):
    return cars_service.create(body)


@router.patch(
    "/{id}",
    summary="Atualiza um carro",
    description="Atualiza parcialmente as informações de um carro.",
    response_model=Car,
    responses=update_car_responses,
)
def update_car(id: uuid.UUID, body: CarUpdate, cars_service: CarsServiceDep):
    try:
        return cars_service.update(id, body)
    except CarNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{id}",
    summary="Remove um carro",
    description="Remove um carro do estoque pelo seu ID.",
    responses=delete_car_responses,
)
def delete_car(id: uuid.UUID, cars_service: CarsServiceDep):
    try:
        cars_service.delete(id)
    except CarNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": f"Carro com id {id} deletado com sucesso."}
