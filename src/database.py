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


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():  # TODO По окончании разработки реализовать миграции на основе alembic
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
