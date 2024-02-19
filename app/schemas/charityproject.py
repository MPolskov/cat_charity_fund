from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator


class CharityProjectBase(BaseModel):
    pass


class CharityProjectCreate(CharityProjectBase):
    name: str
    description: str
    full_amount: int


class CharityProjectUpdate(CharityProjectBase):
    name: str
    description: str
    full_amount: int

    # @validator('name')
    # def name_cant_be_numeric(cls, value: str):
    #     if value is None:
    #         raise ValueError('Имя переговорки не может быть пустым!')
    #     return value


class CharityProjectDB(CharityProjectCreate):
    name: str
    description: str
    full_amount: int
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime

    class Config:
        orm_mode = True