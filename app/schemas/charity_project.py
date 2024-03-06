from typing import Optional
from datetime import datetime

from pydantic import (
    BaseModel, Extra,
    Field, validator,
    PositiveInt, NonNegativeInt
)

from app.msg import ErrorMSG
from app.schemas.constants import (
    MIN_LENGHT_NAME,
    MAX_LENGHT_NAME
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=MIN_LENGHT_NAME,
        max_length=MAX_LENGHT_NAME
    )
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    pass

    @validator('name')
    def name_cant_be_empty(cls, value: str):
        if value is None or value == '':
            raise ValueError(ErrorMSG.NO_NAME)
        return value

    @validator('description')
    def description_cant_be_empty(cls, value: str):
        if value is None or value == '':
            raise ValueError(ErrorMSG.NO_DESCRIPTION)
        return value


class CharityProjectCreate(CharityProjectUpdate):
    name: str = Field(
        ...,
        min_length=MIN_LENGHT_NAME,
        max_length=MAX_LENGHT_NAME
    )
    description: str
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True