import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def _required_url(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing {name}. Copy .env.example and configure the database URL."
        )
    return value


def get_source_engine():
    return create_engine(_required_url("SOURCE_DATABASE_URL"))


def get_target_engine():
    return create_engine(_required_url("TARGET_DATABASE_URL"))
