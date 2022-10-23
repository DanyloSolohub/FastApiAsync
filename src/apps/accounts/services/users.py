from hashlib import sha256

from src.apps.accounts.api.v1.schemas.users import UserCreateSchema, UserUpdateSchema
from src.apps.accounts.exceptions import INACTIVE_USER, USER_NOT_FOUND, USER_ALREADY_EXIST
from src.database.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.engine.cursor import CursorResult


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self) -> list[User]:
        users = await self.session.execute(select(User).where(User.is_active))
        return users.scalars().all()

    async def get_user_or_404(self, user_id: int) -> User:
        user: User = await self.session.get(User, user_id)
        if not user:
            raise USER_NOT_FOUND
        return user

    async def check_user_email(self, email: str):
        user = await self.session.execute(select(User).where(User.email == email))
        user: User = user.scalars().one_or_none()
        if user:
            raise USER_ALREADY_EXIST

    async def get_active_user(self, user_id: int):
        user = await self.get_user_or_404(user_id=user_id)
        if not user.is_active:
            raise INACTIVE_USER
        return user

    async def create_user(self, user: UserCreateSchema) -> User:
        await self.check_user_email(email=user.email)
        user = User(**user.dict())
        self.session.add(user)
        await self.session.commit()
        return await self.get_user_or_404(user_id=user.id)

    async def update_user(self, user_id: int, user: UserUpdateSchema):
        user = await self.get_user_or_404(user_id=user_id)
        if not user.is_active:
            raise INACTIVE_USER
        return user

    async def remove_user(self, user_id: int):
        user: User = await self.get_user_or_404(user_id=user_id)
        await self.session.delete(user)
