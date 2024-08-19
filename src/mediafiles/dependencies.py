from fastapi import UploadFile

from mediafiles.config import mediafiles_settings
from mediafiles.exceptions import MediaFileNotAllowedExtensionError, MediaFileNotFoundError
from mediafiles.schemas import MediaFile
from mediafiles.service import MediaFileService
from mediafiles.utils import check_exists_files, get_file_extension


async def valid_mediafile_uid(mediafile_uid: int) -> MediaFile:
    """Получение записи файла в базе."""
    mediafile = await MediaFileService.get_by_uid(mediafile_uid)
    if not mediafile or not await check_exists_files([mediafile]):
        raise MediaFileNotFoundError
    return mediafile


async def validate_files_type(files: list[UploadFile]) -> list[UploadFile]:
    """Функция для проверки расширений файлов."""
    if not mediafiles_settings.MEDIAFILES_TYPES:
        return files

    for file in files:
        file_extension = get_file_extension(file.filename)
        if file_extension not in mediafiles_settings.MEDIAFILES_TYPES:
            raise MediaFileNotAllowedExtensionError(
                error_message=f"Extension '{file_extension}' not allowed.")
    return files


# Также можно добавить проверку на существование файла по размеру и пути
