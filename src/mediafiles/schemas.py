import datetime

from models import CustomModel


class MediaFile(CustomModel):
    uid: int
    size: int  # размер в bytes
    format: str  # формат ('JPEG', 'MP3')
    original_name: str
    extension: str  # расширение ('.jpg', '.mp3')
    datetime_upload: datetime.datetime
    path: str
    # добавить пользователя
