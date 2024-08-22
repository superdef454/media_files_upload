from fastapi import FastAPI

from config import settings
from mediafiles.exceptions import mediafiles_register_exception_handlers
from mediafiles.router import router as mediafiles_router

app = FastAPI(
    title=settings.TITLE,
    version=settings.APP_VERSION,
    description=settings.DESCRIPTION,
    # root_path="/api",  # Для прокси в случае изменения пути
)

app.include_router(mediafiles_router)
mediafiles_register_exception_handlers(app)
