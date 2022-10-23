from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from src.database.base_class import Base


class DateABC(Base):
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())
