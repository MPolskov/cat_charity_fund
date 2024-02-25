from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.models import User, CharityProject
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationDBSuperUser
)
from app.core.user import current_superuser, current_user
from app.sevices.investing import investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBSuperUser],
    dependencies=[Depends(current_superuser)]

)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получает список всех пожертвований.
    Только для суперюзеров.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationDB,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Вносит новое пожертвование.
    Доступно зарегистрированному пользователю.
    """
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await investing(new_donation, CharityProject, session)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Получает список всех пожертвований для текущего пользователя.
    Доступно зарегистрированному пользователю.
    """
    all_user_donations = await donation_crud.get_donations_by_user(
        user, session
    )
    return all_user_donations