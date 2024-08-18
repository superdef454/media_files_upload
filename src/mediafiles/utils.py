import datetime
import os

import aiofiles
from fastapi import UploadFile

from mediafiles.config import mediafiles_logger, mediafiles_settings
from mediafiles.exceptions import MediaFileUploadError
from mediafiles.schemas import MediaFileAdd


def get_file_path(filename: str) -> str:
    file_path = os.path.join(mediafiles_settings.PATH_TO_SAVE, filename)
    return file_path


def get_file_extension(filename: str) -> str:
    return "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


async def file_save(file: UploadFile) -> MediaFileAdd:
    try:
        file_extension = get_file_extension(file.filename)
        file_path = get_file_path(file.filename)
        contents = await file.read()
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(contents)
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
