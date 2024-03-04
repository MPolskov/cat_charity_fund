from sqlalchemy import Column, String, Text

from app.core.db import Base
from .invest_base import InvestModelBase


class CharityProject(Base, InvestModelBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
