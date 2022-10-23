from fastapi import HTTPException
from starlette import status

UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)
INACTIVE_USER = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user'
)
USER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
)
INCORRECT_PASSWORD = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail='Password incorrect'
)
USER_ALREADY_EXIST = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='User with this email already register'
)
