from typing import Optional

from pydantic import BaseModel, Field, validator


class DonationBase(BaseModel):
    pass


class DonationCreate(DonationBase):
    pass


class DonationUpdate(DonationBase):
    pass

    # @validator('name')
    # def name_cant_be_numeric(cls, value: str):
    #     if value is None:
    #         raise ValueError('Имя переговорки не может быть пустым!')
    #     return value


class DonationDB(DonationCreate):

    class Config:
        orm_mode = True