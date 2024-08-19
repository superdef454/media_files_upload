from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TITLE: str = "MediaFiles"
    DESCRIPTION: str = "Микросервис для приёма, обработки и управления медиафайлами"

    @property
    def database_url_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    REDIS_URL: str

    # SITE_DOMAIN: str = "temp.com"
    # CORS_ORIGINS: list[str]
    # CORS_HEADERS: list[str]

    APP_VERSION: str = "1.0"

    model_config = SettingsConfigDict(env_file=".env")


settings = Config()
