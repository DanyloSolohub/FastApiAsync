from src.database.models.mixins import DateABC
import sqlalchemy as sa
import sqlalchemy_utils as sql_u


class User(DateABC):
    __tablename__ = 'auth_user'
    email = sa.Column(sql_u.EmailType, unique=True, index=True, nullable=False)
    last_name = sa.Column(sa.String(length=255), index=True)
    first_name = sa.Column(sa.String(length=255))
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    is_superuser = sa.Column(sa.Boolean, default=False, nullable=False)
    password = sa.Column(sa.String(length=511), nullable=False)
