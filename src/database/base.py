# Import all the models, so that Base has them before being imported by Alembic

from src.database.base_class import Base  # noqa: F401
from src.database.models.users import User  # noqa: F401
