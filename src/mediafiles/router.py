import datetime

import aiofiles
from fastapi import APIRouter, Depends, File, UploadFile

from mediafiles.config import mediafiles_logger, mediafiles_settings
from mediafiles.dependencies import valid_mediafile_uid
from mediafiles.exceptions import MediaFileNotAllowedExtensionError
from mediafiles.schemas import MediaFile, MediaFileAdd
from mediafiles.service import MediaFileService

router = APIRouter(
    prefix="/mediafiles",
    tags=["mediafiles"],
    )


@router.post("/upload",
             description="Загрузка нескольких файлов на сервер")
async def upload(files: list[UploadFile] = File()) -> list[MediaFile]:
    mediafiles_to_add = []
    for file in files:
        try:
            file_extension = "." + file.filename.rsplit(".", 1)[-1].lower()
            if mediafiles_settings.MEDIAFILES_TYPES and\
            file_extension not in mediafiles_settings.MEDIAFILES_TYPES:
                raise MediaFileNotAllowedExtensionError
            contents = await file.read()
            async with aiofiles.open(file.filename, "wb") as f:
                await f.write(contents)
        except Exception as e:
            await mediafiles_logger.error(f"Error uploading {file.filename}: {e}")
            return {"message": "There was an error uploading the file(s)"}
        else:
            mediafile = MediaFileAdd(
                size=file.size,
                original_name=file.filename,
                extension=file_extension,
                path="/media/photos/photo.jpg",
                datetime_upload=datetime.datetime.now(tz=datetime.timezone.utc),
                format=file_extension,
            )
            await mediafiles_logger.info(f"Successfully uploaded {file.filename}")
            mediafiles_to_add.append(mediafile)
        finally:
            await file.close()
    mediafiles_uploaded = await MediaFileService.add(mediafiles_to_add)
    return mediafiles_uploaded


@router.get("/{mediafile_uid}",
        description="Получение данных о файле по uid")
async def get_mediafile_by_uid(mediafile: MediaFile = Depends(valid_mediafile_uid)) -> MediaFile:
    return mediafile


@router.get("/",
        description="Получить список загруженных файлов")
async def get_all() -> list[MediaFile]:
    mediafiles = await MediaFileService.all()
    return mediafiles
