import logging
import os
from enum import Enum
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)


class EnvironmentEnum(str, Enum):
    PRODUCTION = 'production'
    DEVELOP = 'develop'
    LOCAL = 'local'


class GlobalConfig(BaseSettings):
    TITLE: str = 'Tutorial'
    DESCRIPTION: str = 'Description'

    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False
    TESTING: bool = False
    TIMEZONE: str = 'UTC'

    DATABASE_URL: Optional[
        PostgresDsn
    ] = os.getenv('DATABASE_URL')
    DB_ECHO_LOG: bool = True
    API_V1_STR = '/api/v1'

    @property
    def async_database_url(self) -> Optional[str]:
        return (
            self.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')
            if self.DATABASE_URL
            else self.DATABASE_URL
        )

    class Config:
        case_sensitive = True


class LocalConfig(GlobalConfig):
    """"Local configurations."""

    DEBUG: bool = True
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.LOCAL


class ProdConfig(GlobalConfig):
    """Production configurations."""

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.PRODUCTION


class DevelopConfig(GlobalConfig):
    """Develop configurations."""

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.DEVELOP


class FactoryConfig:
    def __init__(self, environment: Optional[str]):
        self.environment = environment

    def __call__(self) -> GlobalConfig:
        match self.environment:
            case EnvironmentEnum.LOCAL.value:
                return LocalConfig()
            case EnvironmentEnum.DEVELOP.value:
                return DevelopConfig()
            case EnvironmentEnum.PRODUCTION.value:
                return ProdConfig()
            case _:
                raise NotImplementedError


@lru_cache()
def get_configuration() -> GlobalConfig:
    return FactoryConfig(os.getenv('ENVIRONMENT', 'local'))()


configuration = get_configuration()
