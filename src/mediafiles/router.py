import asyncio

from fastapi import APIRouter, Depends, UploadFile

from mediafiles.dependencies import valid_mediafile_uid, validate_files_type
from mediafiles.exceptions import (
    MediaFileNotAllowedExtensionError,
    MediaFileNotFoundError,
    MediaFileUploadError,
    get_responses_code,
)
from mediafiles.schemas import MediaFile, MediaFilesResponse
from mediafiles.service import MediaFileService
from mediafiles.utils import file_save

router = APIRouter(
    prefix="/mediafiles",
    tags=["mediafiles"],
    )


@router.post("/upload",
             description="Загрузка нескольких файлов на сервер",
             responses=get_responses_code([MediaFileNotAllowedExtensionError, MediaFileUploadError]))
async def upload(files: list[UploadFile] = Depends(validate_files_type)) -> MediaFilesResponse:
    mediafiles_to_add = []
    tasks = [asyncio.create_task(file_save(file)) for file in files]
    mediafiles_to_add = await asyncio.gather(*tasks)
    mediafiles_uploaded = await MediaFileService.add(mediafiles_to_add)
    return MediaFilesResponse(data=mediafiles_uploaded)


@router.get("/{mediafile_uid}",
        description="Получение данных о файле по uid",
        responses=get_responses_code([MediaFileNotFoundError]))
async def get_mediafile_by_uid(mediafile: MediaFile = Depends(valid_mediafile_uid)) -> MediaFilesResponse:
    return MediaFilesResponse(data=[mediafile])


@router.get("/",
        description="Получить список загруженных файлов")
async def get_all() -> MediaFilesResponse:
    mediafiles = await MediaFileService.all()
    return MediaFilesResponse(data=mediafiles)
