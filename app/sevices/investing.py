from typing import Union, Type
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing(
        obj: Union[Donation, CharityProject],
        model: Type[Union[Donation, CharityProject]],
        session: AsyncSession
):
    available_items = await session.execute(
        select(model).where(
            model.fully_invested.is_(False)
        ).order_by(
            model.create_date
        )
    )
    available_items = available_items.scalars().all()
    if available_items is None:
        return obj
    for item in available_items:
        obj_remains = obj.full_amount - obj.invested_amount
        item_remains = item.full_amount - item.invested_amount
        if item_remains >= obj_remains:
            obj.invested_amount += obj_remains
            item.invested_amount += obj_remains
            if item.full_amount == item.invested_amount:
                close_object(item)
            session.add(item)
            break
        else:
            item.invested_amount += item_remains
            obj.invested_amount += item_remains
            close_object(item)
            session.add(item)
    if obj.full_amount == obj.invested_amount:
        close_object(obj)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


def close_object(obj):
    obj.fully_invested = True
    obj.close_date = datetime.utcnow()