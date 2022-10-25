from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.accounts.services.users import UserService
from src.database.models.users import User


class AuthService:
    @classmethod
    async def authenticate(cls, session: AsyncSession, email: str, password: str) -> Optional[User]:
        user = await UserService(session=session).get_user_by_email(email=email)
        if not user:
            return None
        if not cls.verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return UserService.get_password_hash(password) == hashed_password
