import asyncio
import datetime
import random

from mediafiles.schemas import MediaFile


class MediaFileService:
    """Сервисный слой для работы со структурой MediaFile."""

    @classmethod
    async def get_by_uid(cls, mediafile_uid: int) -> MediaFile:
        await asyncio.sleep(1)
        # await Tables()...
        mediafile = MediaFile(
            uid=mediafile_uid,
            size=random.randint(4, 8192),
            format="JPEG",
            original_name="photo.jpg",
            extension=".jpg",
            datetime_upload=datetime.datetime.now(tz=datetime.timezone.utc),
            path="/media/photos/photo.jpg",
        )
        return mediafile
