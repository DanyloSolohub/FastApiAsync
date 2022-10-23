from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.paginator import paginate
from src.apps.accounts.api.v1.schemas.users import UserSchema
from src.database.models.users import User
from src.database.session import async_session
from sqlalchemy import select
from fastapi_pagination import Page, Params


async def get_session() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        yield session
        await session.commit()


user_router = APIRouter()


@user_router.get('/', response_model=Page[UserSchema])
async def users(session: AsyncSession = Depends(get_session), params: Params = Depends()):
    all_users = await session.execute(select(User))
    return paginate(
        params=params,
        sequence=[UserSchema(
            id=user.id,
            email=user.email,
            is_active=user.is_active
        ) for user in all_users.scalars().all()],
    )
