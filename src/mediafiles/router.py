import asyncio

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse

from mediafiles.config import mediafiles_settings
from mediafiles.dependencies import valid_mediafile_uid, validate_files_type
from mediafiles.exceptions import (
    MediaFileNotAllowedExtensionError,
    MediaFileNotFoundError,
    MediaFileUploadError,
    get_responses_code,
)
from mediafiles.schemas import MediaFile, MediaFilesResponse
from mediafiles.service import MediaFileService
from mediafiles.utils import check_exists_files, file_save
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
    # Не очень понял пункт (Отправка в облако: Копия файла должна быть асинхронно отправлена в облачное хранилище.)
    # Если требуется только асинхронность, то вот функция:
    # async def file_save_and_upload(file: UploadFile, cloud_client: CloudClient) -> MediaFileAdd:
    #     mediafile = await file_save(file)  # Сохранение файла на сервере
    #     await cloud_client.upload_file(mediafile.path)  # Отправка файла в облако
    #     return mediafile
    # Но вместо этого хотелось бы вынести загрузку файлов в облако в фон с помощью celery
    process_cloud_uploaded.delay([mediafile.path for mediafile in mediafiles_uploaded])
    return MediaFilesResponse(data=mediafiles_uploaded)


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
