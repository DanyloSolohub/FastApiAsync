from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    email: EmailStr
    last_name: str = ''
    first_name: str = ''


class PasswordSchema(BaseModel):
    password: str


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool


class UserCreateSchema(UserBaseSchema, PasswordSchema):
    is_active: bool = True


class UserUpdateSchema(BaseModel):
    passwd: Optional[str] = None
    is_active: bool
    last_name: str
    first_name: str
