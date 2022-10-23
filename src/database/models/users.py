from src.database.models.mixins import DateABC
import sqlalchemy as sa
import sqlalchemy_utils as sql_u


class User(DateABC):
    __tablename__ = 'auth_user'
    email = sa.Column(sql_u.EmailType, unique=True, nullable=False)
    is_active = sa.Column(sa.Boolean, server_default=sa.sql.expression.false(), nullable=False)
    is_superuser = sa.Column(sa.Boolean, server_default=sa.sql.expression.false(), nullable=False)
    password = sa.Column(sa.String(length=511), nullable=False)
