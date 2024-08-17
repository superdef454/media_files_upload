from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from database import create_tables, delete_tables
from mediafiles.router import router as mediafiles_router

# FastAPI - не мой основной фреймворк и всех тонкостей могу не учесть, прошу оставить комментарии по улучшению коду


@asynccontextmanager
async def lifespan(app: FastAPI):  # TODO alemdic
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(
    title=settings.TITLE,
    version=settings.APP_VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    # root_path="/api",  # Для прокси в случае изменения пути
)

app.include_router(mediafiles_router)
