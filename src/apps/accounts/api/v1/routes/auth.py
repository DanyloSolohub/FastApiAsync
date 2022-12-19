from fastapi import Depends, Security, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.accounts.api.v1.schemas.auth import LoginSchema
from src.apps.accounts.api.v1.schemas.users import UserSchema
from src.apps.accounts.exceptions import BAD_CREDENTIALS
from src.apps.accounts.services.auth import AuthService
from src.database.models.users import User
from src.database.session import get_session
from fastapi_auth0 import Auth0, Auth0User
from src.settings.config import configuration

auth_router = APIRouter(prefix='/accounts', tags=['auth'])
auth = Auth0(domain=configuration.DOMAIN, api_audience=configuration.API_AUDIENCE)


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


@auth_router.get("/public")
async def get_public():
    return {"message": "Anonymous user"}


@auth_router.get("/secure", dependencies=[Depends(auth.implicit_scheme)])
async def get_secure(user: Auth0User = Security(auth.get_user)):
    print(user.email)
    print(dir(user))
    return {"message": f"{user}"}


# @auth_router.get("/secure/blabla", dependencies=[Depends(auth.implicit_scheme)])
# async def get_secure_scoped(user: Auth0User = Security(auth.get_user)):
#     return {"message": f"{user}"}
#
#
# @auth_router.get("/secure/blabla2")
# async def get_secure_scoped2(user: Auth0User = Security(auth.get_user)):
#     return {"message": f"{user}"}
