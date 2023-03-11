from pydantic import BaseModel, BaseSettings


class SASettings(BaseModel):
    drivername: str
    username: str | None = None
    password: str | None = None
    host: str | None = None
    port: int | None = None
    database: str | None = None
    echo: bool = True


class DBSettings(BaseSettings):
    class Config:
        env_nested_delimiter = "__"
        env_prefix = "kittens_"
        env_file = ".env"

    sa_settings: SASettings


def get_settlings(env_file: str | None = None) -> DBSettings:
    if env_file:
        return DBSettings(_env_file=env_file)  # type: ignore
    else:
        return DBSettings()  # type: ignore
