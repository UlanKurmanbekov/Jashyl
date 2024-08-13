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
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    ADMIN: int = os.getenv('ADMIN')


class DataBaseConfig(BaseModel):
    url: str = os.getenv('DB_URL')


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    db: DataBaseConfig


settings = Settings()
