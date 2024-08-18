import datetime

from pydantic import ConfigDict

from models import BaseResponse, CustomModel


class MediaFileAdd(CustomModel):
    size: int  # размер в bytes
    format: str  # формат ('JPEG', 'MP3')
    original_name: str
    extension: str  # расширение ('.jpg', '.mp3')
    datetime_upload: datetime.datetime
    path: str
    # добавить пользователя


class MediaFile(MediaFileAdd):
    uid: int

    model_config = ConfigDict(from_attributes=True)


class MediaFilesResponse(BaseResponse):
    data: list[MediaFile] = []
