import logging
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


def configure_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s',
    )


class RunConfig(BaseModel):
    bot_token: str
    admin: int


class DataBaseConfig(BaseModel):
    url: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env.template', '.env'),
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='BOT_CONFIG__'
    )
    run: RunConfig
    db: DataBaseConfig


settings = Settings()
