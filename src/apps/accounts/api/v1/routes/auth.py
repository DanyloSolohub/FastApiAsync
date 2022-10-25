from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.accounts.api.v1.schemas.auth import LoginSchema
from src.apps.accounts.api.v1.schemas.users import UserSchema
from src.apps.accounts.exceptions import BAD_CREDENTIALS
from src.apps.accounts.services.auth import AuthService
from src.database.models.users import User
from src.database.session import get_session

auth_router = APIRouter(prefix='/accounts', tags=['auth'])


@auth_router.post('/login', response_model=UserSchema)
async def login(user_login: LoginSchema, session: AsyncSession = Depends(get_session)):
    user = await AuthService.authenticate(
        session=session,
        email=user_login.email,
        password=user_login.password
    )
    if not user or not isinstance(user, User):
        raise BAD_CREDENTIALS
    return UserSchema(**jsonable_encoder(user))
