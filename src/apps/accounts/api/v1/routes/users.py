from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.paginator import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.apps.accounts.api.v1.schemas.users import UserSchema, UserCreateSchema, UserUpdateSchema
from src.apps.accounts.services.users import UserService
from src.database.session import get_session

user_router = APIRouter()


@user_router.get('/', response_model=Page[UserSchema])
async def users(session: AsyncSession = Depends(get_session), params: Params = Depends()):
    all_users = await UserService(session=session).get_all_users()
    return paginate(
        params=params,
        sequence=[UserSchema(**user.__dict__) for user in all_users],
    )


@user_router.post('/', response_model=UserSchema)
async def users(user: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    user = await UserService(session=session).create_user(user=user)
    return UserSchema(**user.__dict__)


@user_router.patch('/{user_id}', response_model=UserSchema)
async def users(user_id: int, user: UserUpdateSchema, session: AsyncSession = Depends(get_session)):
    user = await UserService(session=session).update_user(user_id=user_id, user=user)
    return UserSchema(**user.__dict__)


@user_router.get('/{user_id}', response_model=UserSchema)
async def users(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await UserService(session=session).get_active_user(user_id=user_id)
    return UserSchema(**user.__dict__)


@user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def users(user_id: int, session: AsyncSession = Depends(get_session)):
    await UserService(session=session).remove_user(user_id=user_id)
