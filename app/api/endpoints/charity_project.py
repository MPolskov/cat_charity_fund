from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate
)
from app.api.validators import (
    check_name_duplicate,
    check_project_exists,
    check_invested_amount_delete,
    check_full_amount_update,
    check_close_project
)
from app.services.investing import investing
from app.models import Donation

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получает список всех проектов.
    Досутпно любому пользователюю
    """
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создает новый проект.
    Только для суперюзеров.
    """
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    return await investing(new_project, Donation, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Удаляет указанный проект.
    Нельзя удалить проект в который уже внесены пожертвования
    или проект закрыт.
    Только для суперюзеров.
    """
    project = await check_project_exists(project_id, session)
    await check_invested_amount_delete(project)
    await check_close_project(project)
    return await charity_project_crud.remove(project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Изменяет указанный проект.
    Только для суперюзеров.
    """
    project = await check_project_exists(
        project_id, session
    )
    await check_close_project(project)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_full_amount_update(project, obj_in.full_amount)
    return await charity_project_crud.update(project, obj_in, session)