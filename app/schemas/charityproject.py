from typing import Optional

from pydantic import BaseModel, Field, validator


class CharityProjectBase(BaseModel):
    pass


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    pass

    # @validator('name')
    # def name_cant_be_numeric(cls, value: str):
    #     if value is None:
    #         raise ValueError('Имя переговорки не может быть пустым!')
    #     return value


class CharityProjectDB(CharityProjectCreate):

    class Config:
        orm_mode = True