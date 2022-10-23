from fastapi import APIRouter

from src.apps.accounts.api.v1.routes.users import user_router

api_v1_router = APIRouter()
api_v1_router.include_router(user_router, prefix='/users', tags=['users'])
