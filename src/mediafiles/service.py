from sqlalchemy import select

from database import async_sessions
from mediafiles.models import MediaFileOrm
from mediafiles.schemas import MediaFile, MediaFileAdd


class MediaFileService:
    """Сервисный слой для работы со структурой MediaFileOrm."""
    @classmethod
    async def add(cls, mediafiles_data: list[MediaFileAdd]) -> list[MediaFile]:
        async with async_sessions() as session:
            mediafiles_add = [MediaFileOrm(**mediafile.model_dump()) for mediafile in mediafiles_data]
            session.add_all(mediafiles_add)
            await session.flush()
            await session.commit()
            mediafile_schemas = [MediaFile.model_validate(mediafile) for mediafile in mediafiles_add]
            return mediafile_schemas

    @classmethod
    async def all(cls) -> list[MediaFile]:
        async with async_sessions() as session:
            query = select(MediaFileOrm)
            result = await session.execute(query)
            mediafile_models = result.scalars().all()
            mediafile_schemas = [MediaFile.model_validate(mediafile) for mediafile in mediafile_models]
            return mediafile_schemas

    @classmethod
    async def get_by_uid(cls, mediafile_uid: int) -> MediaFile:
        async with async_sessions() as session:
            mediafile_model = await session.get(MediaFileOrm, mediafile_uid)
            mediafile_schema = MediaFile.model_validate(mediafile_model)
            return mediafile_schema
