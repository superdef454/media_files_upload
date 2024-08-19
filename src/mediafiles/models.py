import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Model


class MediaFileOrm(Model):
    __tablename__ = "mediafile"

    uid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    format: Mapped[str] = mapped_column(String, nullable=False)
    original_name: Mapped[str] = mapped_column(String, nullable=False)
    extension: Mapped[str] = mapped_column(String, nullable=False)
    datetime_upload: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
    path: Mapped[str] = mapped_column(String, nullable=False)
    # Также можно использовать fastapi-storages в случае необходимости сохранения напрямую в облачное хранилище

    def __repr__(self) -> str:
        return f"<MediaFileOrm(uid={self.uid}, original_name='{self.original_name}', format='{self.format}')>"
