import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject, Donation


async def investing_in_new_project(
    project: CharityProject,
    session: AsyncSession
):
    available_donats = await session.execute(
        select(Donation).where(
            Donation.fully_invested == False
        ).order_by(
            Donation.create_date
        )
    )
    available_donats = available_donats.scalars().all()
    if available_donats is None:
        return project
    for donat in available_donats:
        proj_remains = project.full_amount - project.invested_amount
        donat_remains = donat.full_amount - donat.invested_amount
        if proj_remains <= donat_remains:
            donat.invested_amount += proj_remains
            project.invested_amount += proj_remains
            if donat.full_amount == donat.invested_amount:
                donat.fully_invested = True
                donat.close_date = datetime.utcnow()
            session.add(donat)
            break
        else:
            project.invested_amount += donat_remains
            donat.fully_invested = True
            donat.close_date = datetime.utcnow()
            session.add(donat)
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.utcnow()
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project
