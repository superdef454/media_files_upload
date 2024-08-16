import aiofiles
from fastapi import APIRouter, Depends, File, UploadFile

from mediafiles.config import mediafiles_logger
from mediafiles.dependencies import valid_mediafile_uid
from mediafiles.schemas import MediaFile

router = APIRouter(
    prefix="/mediafiles",
    )


@router.post("/upload",
             description="Загрузка нескольких файлов на сервер",
             )  # , response_model=MediaFilesResponse)
async def upload(files: list[UploadFile] = File()) -> dict:
    files_uploaded = []
    for file in files:
        try:
            contents = await file.read()
            async with aiofiles.open(file.filename, "wb") as f:
                await f.write(contents)
        except Exception as e:
            await mediafiles_logger.error(f"Error uploading {file.filename}: {e}")
            return {"message": "There was an error uploading the file(s)"}
        finally:
            await mediafiles_logger.info(f"Successfully uploaded {file.filename}")
            await file.close()
            files_uploaded.append(file.filename)

    return {"message": f"Successfuly uploaded {files_uploaded}"}


@router.get("/{mediafile_uid}")  # , response_model=MediaFilesResponse)
async def get_mediafile_by_uid(mediafile: MediaFile = Depends(valid_mediafile_uid)) -> MediaFile:
    return mediafile
