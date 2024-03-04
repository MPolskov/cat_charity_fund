from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from .invest_base import InvestModelBase


class Donation(Base, InvestModelBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)