import datetime

from pydantic import ConfigDict, model_validator

from mediafiles.config import mediafiles_settings
from models import BaseResponse, CustomModel


class MediaFileAdd(CustomModel):
    size: int
    format: str  # ('image/jpeg',)
    original_name: str
    extension: str  # расширение ('.jpg', '.mp3')
    datetime_upload: datetime.datetime
    path: str
    # Также можно реализовать хранение пользователя, который загрузил в случае реализации авторизации


class MediaFile(MediaFileAdd):
    uid: int
    url: str = ""  # Помимо метода download_mediafile_by_uid добавлено поле URL
    # т.к. в docker-compose настроен NGINX способный отдавать файл и настроены пути

    @model_validator(mode="after")
    def set_url(cls, values):
        values.url = f"{mediafiles_settings.SERVER_URL}{values.path}"
        return values

    model_config = ConfigDict(from_attributes=True)


class MediaFilesResponse(BaseResponse):
    data: list[MediaFile] = []
