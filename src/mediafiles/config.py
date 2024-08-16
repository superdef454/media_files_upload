from aiologger.loggers.json import JsonLogger
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    MEDIAFILES_TYPES: list[str] = [".jpeg", ".mp3"]  # TODO Добавить доверенные расширения файлов


mediafiles_settings = Config()

mediafiles_logger = JsonLogger.with_default_handlers()
