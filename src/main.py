from fastapi import FastAPI

from config import settings
from mediafiles.router import router as mediafiles_router

# FastAPI - не мой основной фреймворк и всех тонкостей могу не учесть, прошу оставить комментарии по улучшению коду

app = FastAPI(
    title=settings.TITLE,
    version=settings.APP_VERSION,
    description=settings.DESCRIPTION,
    # root_path="/api",  # Для прокси в случае изменения пути
)

app.include_router(mediafiles_router)
