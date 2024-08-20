from typing import Annotated

from sqlalchemy import String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

async_engine = create_async_engine(
    url=settings.database_url_asyncpg,
    # echo=True,
)

async_sessions = async_sessionmaker(async_engine, expire_on_commit=False)

str_256 = Annotated[str, 256]


class Model(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256),
    }
