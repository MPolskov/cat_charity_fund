from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        return db_obj

    async def get_donations_by_user(
            self,
            user: User,
            session: AsyncSession
    ):
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)