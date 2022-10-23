from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    email: EmailStr


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool


class UserCreateSchema(UserBaseSchema):
    password: str
    is_active: bool = True


class UserUpdateSchema(UserBaseSchema):
    password: str
    is_active: bool = True
