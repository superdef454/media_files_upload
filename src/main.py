from fastapi import FastAPI

from config import settings
from mediafiles.exceptions import mediafiles_register_exception_handlers
from mediafiles.router import router as mediafiles_router

# FastAPI - не мой основной фреймворк и всех тонкостей могу не учесть, прошу оставить комментарии по улучшению коду
# Делал после основного проекта, на возможные ошибки прошу отнестись с пониманием =)


app = FastAPI(
    title=settings.TITLE,
    version=settings.APP_VERSION,
    description=settings.DESCRIPTION,
    # root_path="/api",  # Для прокси в случае изменения пути
)

app.include_router(mediafiles_router)
mediafiles_register_exception_handlers(app)
