import asyncio
import datetime

import aiofiles
from fastapi import APIRouter, Depends, UploadFile, WebSocket
from fastapi.responses import FileResponse

from mediafiles.config import mediafiles_logger, mediafiles_settings
from mediafiles.dependencies import valid_mediafile_uid, validate_files_type
from mediafiles.exceptions import (
    MediaFileNotAllowedExtensionError,
    MediaFileNotFoundError,
    MediaFileUploadError,
    get_responses_code,
)
from mediafiles.schemas import MediaFile, MediaFileAdd, MediaFilesResponse
from mediafiles.service import MediaFileService
from mediafiles.utils import check_exists_files, file_save, get_file_extension, get_file_path
from mediafiles.worker import process_cloud_uploaded

router = APIRouter(
    prefix="/mediafiles",
    tags=["mediafiles"],
    )


@router.post("/upload",
             description=f"Загрузка нескольких файлов на сервер"
              f"{f' ({mediafiles_settings.MEDIAFILES_TYPES})' if mediafiles_settings.MEDIAFILES_TYPES else ''}",
             responses=get_responses_code([MediaFileNotAllowedExtensionError, MediaFileUploadError]))
async def upload(files: list[UploadFile] = Depends(validate_files_type)) -> MediaFilesResponse:
    mediafiles_to_add = []
    tasks = [asyncio.create_task(file_save(file)) for file in files]
    mediafiles_to_add = await asyncio.gather(*tasks)
    mediafiles_uploaded = await MediaFileService.add(mediafiles_to_add)
    process_cloud_uploaded.delay([mediafile.model_dump() for mediafile in mediafiles_uploaded])
    return MediaFilesResponse(data=mediafiles_uploaded)


@router.websocket("/upload/ws")
async def upload_ws(websocket: WebSocket):
    mediafiles_to_add = []
    await websocket.accept()
    try:
        while True:
            # Получаем название
            filename = await websocket.receive_text()
            if filename == "END":
                break
            file_path = get_file_path(filename)
            file_extension = get_file_extension(filename)
            size = 0
            # Получаем файл
            async with aiofiles.open(file_path, "wb") as out_file:
                while content := await websocket.receive_bytes():
                    size += len(content)
                    await out_file.write(content)
            mediafile = MediaFileAdd(
                size=size,
                original_name=filename,
                extension=file_extension,
                path=file_path,
                datetime_upload=datetime.datetime.now(tz=datetime.timezone.utc),
                format="application/octet-stream",
            )
            mediafiles_to_add.append(mediafile)
            await mediafiles_logger.info(f"Successfully uploaded {filename}")
    except Exception as e:
        await mediafiles_logger.error(f"Error uploading {filename}: {e}")
    finally:
        await websocket.close()
    mediafiles_uploaded = await MediaFileService.add(mediafiles_to_add)
    process_cloud_uploaded.delay([mediafile.model_dump() for mediafile in mediafiles_uploaded])


@router.get("/{mediafile_uid}",
        description="Получение данных о файле по uid",
        responses=get_responses_code([MediaFileNotFoundError]))
async def get_mediafile_by_uid(mediafile: MediaFile = Depends(valid_mediafile_uid)) -> MediaFilesResponse:
    return MediaFilesResponse(data=[mediafile])


@router.get("/download/{mediafile_uid}",
        description="Метод для скачивания файла по uid",
        responses=get_responses_code([MediaFileNotFoundError]))
async def download_mediafile_by_uid(mediafile: MediaFile = Depends(valid_mediafile_uid)) -> FileResponse:
    return FileResponse(path=mediafile.path, filename=mediafile.original_name, media_type=mediafile.format or
                        "application/octet-stream")


@router.get("/",
        description="Получить список загруженных файлов")
async def get_all() -> MediaFilesResponse:
    mediafiles = await MediaFileService.all()
    verified_mediafiles = await check_exists_files(mediafiles)
    return MediaFilesResponse(data=verified_mediafiles)
