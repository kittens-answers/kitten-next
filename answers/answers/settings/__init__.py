from pydantic import BaseSettings as PydanticBaseSettings


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_nested_delimiter = "__"
        env_prefix = "kittens_"
        env_file = ".env"
