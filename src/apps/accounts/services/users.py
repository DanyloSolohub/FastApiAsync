from hashlib import sha256

from fastapi import Depends

from apps.accounts.api.v1.schemas.users import UserCreateSchema
from apps.accounts.exceptions import INACTIVE_USER, USER_NOT_FOUND
from database.models.users import User
from database.session import async_session


async def get_user_or_404(user_id: str) -> User:
    user_instance: User = await async_session.object_session(User).get(User, user_id)
    if not user_instance:
        raise USER_NOT_FOUND
    print(user_instance)
    return user_instance


def get_current_active_user(current_user: User = Depends(get_user_or_404)):
    if not current_user.is_active:
        raise INACTIVE_USER
    return current_user


async def create_user(user: UserCreateSchema) -> User:
    user_instance: User = await async_session.get(User, user_id)
    return User.create(email=user.email, password=sha256(user.password.encode('utf-8')).hexdigest())
