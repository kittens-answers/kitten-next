from enum import StrEnum

from pydantic import BaseSettings as PydanticBaseSettings


class DBTypeEnum(StrEnum):
    SQLALCHEMY = "SQLALCHEMY"


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_nested_delimiter = "__"
        env_prefix = "kittens_"
        env_file = ".env"


class BootStrapSettings(BaseSettings):
    db_type: DBTypeEnum
