from aiologger.loggers.json import JsonLogger
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    MEDIAFILES_TYPES: list[str] = [".jpeg", ".jpg", ".mp3"]  # TODO Добавить доверенные расширения файлов
    PATH_TO_SAVE: str = "/media"


mediafiles_settings = Config()

mediafiles_logger = JsonLogger.with_default_handlers()
