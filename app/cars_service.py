import uuid

from app.exceptions import CarNotFoundError
from app.models import CarCreate, CarUpdate


class CarsService:
    def __init__(self):
        self._cars = [
            {
                "id": uuid.uuid4(),
                "brand": "Toyota",
                "model": "Corolla",
            },
            {
                "id": uuid.uuid4(),
                "brand": "Honda",
                "model": "Civic",
            },
            {
                "id": uuid.uuid4(),
                "brand": "Jeep",
                "model": "Cherokee",
            },
        ]

    def find_all(self):
        return self._cars

    def find_one_by_id(self, id: uuid.UUID):
        for car in self._cars:
            if car["id"] == id:
                return car
        raise CarNotFoundError(id)

    def create(self, body: CarCreate):
        new_car = {
            "id": uuid.uuid4(),
            "brand": body.brand,
            "model": body.model,
        }
        self._cars.append(new_car)
        return new_car

    def update(self, id: uuid.UUID, body: CarUpdate):
        car = self.find_one_by_id(id)
        if body.brand is not None:
            car["brand"] = body.brand
        if body.model is not None:
            car["model"] = body.model

        return car

    def delete(self, id: uuid.UUID):
        self.find_one_by_id(id)
        self._cars = [car for car in self._cars if car["id"] != id]
