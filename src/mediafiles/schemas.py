import datetime

from pydantic import ConfigDict

from models import BaseResponse, CustomModel


class MediaFileAdd(CustomModel):
    size: int
    format: str
    original_name: str
    extension: str
    datetime_upload: datetime.datetime
    path: str
    # Также можно реализовать хранение пользователя, который загрузил в случае реализации авторизации


class MediaFile(MediaFileAdd):
    uid: int

    model_config = ConfigDict(from_attributes=True)


class MediaFilesResponse(BaseResponse):
    data: list[MediaFile] = []
