from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_donations_by_user(
            self,
            user: User,
            session: AsyncSession
    ):
        donations = session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations

    # async def get_room_id_by_name(
    #         self,
    #         room_name: str,
    #         session: AsyncSession,
    # ) -> Optional[int]:
    #     db_room_id = await session.execute(
    #         select(MeetingRoom.id).where(
    #             MeetingRoom.name == room_name
    #         )
    #     )
    #     db_room_id = db_room_id.scalars().first()
    #     return db_room_id


donation_crud = CRUDDonation(Donation)