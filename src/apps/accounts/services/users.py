import re
from hashlib import sha256

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.accounts.api.v1.schemas.users import UserCreateSchema, UserUpdateSchema
from src.apps.accounts.exceptions import INACTIVE_USER, USER_NOT_FOUND, USER_ALREADY_EXIST, INCORRECT_PASSWORD
from src.database.models.users import User


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

    async def get_user_by_email(self, email: str) -> User:
        user = await self.session.execute(select(User).where(User.email == email))
        user: User = user.scalars().one_or_none()
        return user

    async def get_active_user(self, user_id: int):
        user = await self.get_user_or_404(user_id=user_id)
        if not user.is_active:
            raise INACTIVE_USER
        return user

    async def create_user(self, serialized_data: UserCreateSchema) -> User:
        user = await self.get_user_by_email(email=serialized_data.email)
        if user:
            raise USER_ALREADY_EXIST
        self.validate_password(serialized_data.password)
        serialized_data.password = self.get_password_hash(serialized_data.password)
        result = await self.session.execute(insert(User).values(**serialized_data.dict()))
        pk = result.inserted_primary_key
        return await self.get_user_or_404(user_id=pk)

    async def update_user(self, db_user: User, serialized_user: UserUpdateSchema):
        update_data = serialized_user.dict()
        if update_data['passwd']:
            password = self.validate_password(update_data['passwd'])
            del update_data['passwd']
            update_data['password'] = self.get_password_hash(password)
        for field in update_data:
            if field in update_data:
                setattr(db_user, field, update_data[field])
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def remove_user(self, user_id: int):
        user: User = await self.get_user_or_404(user_id=user_id)
        await self.session.delete(user)

    @staticmethod
    def get_password_hash(password):
        return sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def validate_password(password):
        regex = r'((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,40})\S$'
        result = re.findall(regex, password)
        if not result:
            raise INCORRECT_PASSWORD
        return password
