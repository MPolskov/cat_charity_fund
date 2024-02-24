from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB
)
# from app.api.validators import ()
from app.core.user import current_superuser, current_user

router = APIRouter()


@router.get(
    '/',
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    # TODO add validators
    new_donation = await donation_crud.create(donation, session, user)
    return new_donation


@router.get(
    '/my',
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получает список всех пожертвований для текущего пользователя."""
    all_user_donations = await donation_crud.get_donations_by_user(
        user, session
    )
    return all_user_donations