from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.settings.config import configuration

engine = create_async_engine(
    configuration.async_database_url,
    echo=configuration.DB_ECHO_LOG,
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        yield session
        await session.commit()
