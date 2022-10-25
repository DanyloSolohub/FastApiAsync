from fastapi import APIRouter, Depends, Body
from fastapi_pagination import Page, Params
from fastapi_pagination.paginator import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.apps.accounts.api.v1.schemas.users import UserSchema, UserCreateSchema, UserUpdateSchema
from src.apps.accounts.services.users import UserService
from src.database.session import get_session
from fastapi.encoders import jsonable_encoder

user_router = APIRouter(prefix='/users', tags=['auth'])


@user_router.get('/', response_model=Page[UserSchema], status_code=status.HTTP_200_OK)
async def users(session: AsyncSession = Depends(get_session), params: Params = Depends()):
    all_users = await UserService(session=session).get_all_users()
    return paginate(
        params=params,
        sequence=[UserSchema(**jsonable_encoder(user)) for user in all_users],
    )


@user_router.post('/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    user = await UserService(session=session).create_user(serialized_data=user)
    return UserSchema(**jsonable_encoder(user))


@user_router.patch('/{user_id}', response_model=UserSchema, status_code=status.HTTP_200_OK)
async def update_user(
        user_id: int,
        passwd: str = Body(None),
        is_active: bool = Body(None),
        last_name: str = Body(None),
        first_name: str = Body(None),
        session: AsyncSession = Depends(get_session)
):
    user_service = UserService(session=session)
    user = await user_service.get_active_user(user_id=user_id)
    user_in = UserUpdateSchema(**jsonable_encoder(user))
    if passwd is not None:
        user_in.passwd = passwd
    if is_active is not None:
        user_in.is_active = is_active
    if last_name is not None:
        user_in.last_name = last_name
    if first_name is not None:
        user_in.first_name = first_name
    user = await user_service.update_user(db_user=user, serialized_user=user_in)
    return UserSchema(**jsonable_encoder(user))


@user_router.get('/{user_id}', response_model=UserSchema)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await UserService(session=session).get_active_user(user_id=user_id)
    return UserSchema(**jsonable_encoder(user))


@user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    await UserService(session=session).remove_user(user_id=user_id)
