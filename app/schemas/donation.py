from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator


class DonationBase(BaseModel):
    pass


class DonationCreate(DonationBase):
    full_amount: int
    comment: Optional[str]


class DonationUpdate(DonationBase):
    pass

    # @validator('name')
    # def name_cant_be_numeric(cls, value: str):
    #     if value is None:
    #         raise ValueError('Имя переговорки не может быть пустым!')
    #     return value


class DonationDB(DonationCreate):
    full_amount: int
    comment: Optional[str]
    id: int
    create_date: datetime

    class Config:
        orm_mode = True