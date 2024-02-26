from http import HTTPStatus
from enum import Enum

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


class ErrorMSG(str, Enum):
    EXIST = 'Проект с таким именем уже существует!'
    NOT_FOUND = 'Проект не найден!'
    INVESTED = 'В проект были внесены средства, не подлежит удалению!'
    BELOW_DEPOSIT = 'Нелья установить значение full_amount меньше уже вложенной суммы.'
    CLOSED = 'Закрытый проект нельзя редактировать!'


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    room_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if room_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMSG.EXIST
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorMSG.NOT_FOUND
        )
    return project


async def check_invested_amount_delete(
        project: CharityProject
) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMSG.INVESTED
        )


async def check_full_amount_update(
        project: CharityProject,
        new_amount: int
) -> None:
    if project.invested_amount > new_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMSG.BELOW_DEPOSIT
        )


async def check_close_project(
        project: CharityProject
) -> None:
    if project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMSG.CLOSED
        )