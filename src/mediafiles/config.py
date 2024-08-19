from aiologger.loggers.json import JsonLogger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    MEDIAFILES_TYPES: list[str] = []
    PATH_TO_SAVE: str = "/media"  # Проверить доступ
    CLOUD_URL: str = ""
    SERVER_URL: str = ""

    model_config = SettingsConfigDict(env_file=".env.mediafiles")



mediafiles_settings = Config()

mediafiles_logger = JsonLogger.with_default_handlers()  # TODO Настроить логер в единую папку logs и для каждого модуля определить свой файл
