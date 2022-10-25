from fastapi import APIRouter

from src.apps.accounts.api.v1.routes.users import user_router
from src.apps.accounts.api.v1.routes.auth import auth_router

api_v1_router = APIRouter()
api_v1_router.include_router(user_router, prefix='/users', tags=['users'])
api_v1_router.include_router(auth_router, prefix='/accounts', tags=['auth'])
