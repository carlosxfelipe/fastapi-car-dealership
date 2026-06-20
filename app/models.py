from pydantic import BaseModel, Field


class Car(BaseModel):
    id: int
    brand: str
    model: str


class CarCreate(BaseModel):
    brand: str = Field(min_length=2)
    model: str = Field(min_length=2)


class CarCreateResponse(BaseModel):
    status: str
    car: Car
