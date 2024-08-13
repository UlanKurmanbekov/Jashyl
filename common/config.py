import os
import logging
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings


load_dotenv()


def configure_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s',
    )


class RunConfig(BaseModel):
    BOT_TOKEN: str
    ADMIN: int


class DataBaseConfig(BaseModel):
    url: str
    echo: bool = False
    echo_pool: bool = False,
    pool_size: int = 50,
    max_overflow: int = 10,


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    db: DataBaseConfig


settings = Settings()
