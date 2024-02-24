from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator, PositiveInt, NonNegativeInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(..., min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass

    @validator('name')
    def name_cant_be_empty(cls, value: str):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value

    @validator('description')
    def description_cant_be_empty(cls, value: str):
        if value is None:
            raise ValueError('Описание проекта не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True