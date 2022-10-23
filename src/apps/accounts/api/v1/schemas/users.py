from pydantic import BaseModel, EmailStr, validator
import re
from hashlib import sha256

from src.apps.accounts.exceptions import INCORRECT_PASSWORD


class UserBaseSchema(BaseModel):
    email: EmailStr


class PasswordSchema(BaseModel):
    password: str

    @validator('password')
    def passwords_match(cls, password, **kwargs):
        regex = r'((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,40})\S$'
        result = re.findall(regex, password)
        if not result:
            raise INCORRECT_PASSWORD
        return sha256(password.encode('utf-8')).hexdigest()


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool


class UserCreateSchema(UserBaseSchema, PasswordSchema):
    is_active: bool = True


class UserUpdateSchema(PasswordSchema):
    is_active: bool = True
