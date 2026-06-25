from typing import Optional
from uuid import UUID

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(extra="forbid")


class Car(BaseModel):
    id: UUID
    brand: str
    model: str


class CarCreate(BaseModel):
    brand: str = Field(min_length=2)
    model: str = Field(min_length=2)


class CarUpdate(BaseModel):
    brand: Optional[str] = Field(default=None, min_length=2)
    model: Optional[str] = Field(default=None, min_length=2)
