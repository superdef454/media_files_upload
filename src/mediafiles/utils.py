import datetime
import os

import aiofiles
from fastapi import UploadFile

from mediafiles.config import mediafiles_logger, mediafiles_settings
from mediafiles.exceptions import MediaFileUploadError
from mediafiles.schemas import MediaFile, MediaFileAdd
from mediafiles.service import MediaFileService
from models import datetime_to_gmt_str


def get_file_path(filename: str) -> str:
    file_path = os.path.join(mediafiles_settings.PATH_TO_SAVE,
                             f"{datetime_to_gmt_str(datetime.datetime.now(datetime.timezone.utc))}_{filename}")
    return file_path


def get_file_extension(filename: str) -> str:
    return "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


async def check_exists_files(mediafiles: list[MediaFile]) -> list[MediaFile]:
    verified_mediafiles = []
    for mediafile in mediafiles:
        if not os.path.exists(mediafile.path):
            await MediaFileService.delete_by_uid(mediafile.uid)
            await mediafiles_logger.error(f"File not found and delete in DB({mediafile.uid}): {mediafile.path}")
        else:
            verified_mediafiles.append(mediafile)
    return verified_mediafiles


async def file_save(file: UploadFile) -> MediaFileAdd:
    try:
        file_extension = get_file_extension(file.filename)
        file_path = get_file_path(file.filename)

        async with aiofiles.open(file_path, "wb") as out_file:
            while content := await file.read(1024):
                await out_file.write(content)

    except Exception as e:
        await mediafiles_logger.error(f"Error uploading {file.filename}: {e}")
        raise MediaFileUploadError from e
    else:
        mediafile = MediaFileAdd(
            size=file.size,
            original_name=file.filename,
            extension=file_extension,
            path=file_path,
            datetime_upload=datetime.datetime.now(tz=datetime.timezone.utc),
            format=file.content_type,
        )
        await mediafiles_logger.info(f"Successfully uploaded {file.filename}")
        return mediafile
    finally:
        await file.close()
