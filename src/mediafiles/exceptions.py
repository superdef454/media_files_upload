from dataclasses import dataclass

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from mediafiles.schemas import MediaFilesResponse
from models import BaseError


@dataclass
class MediaFileUploadError(BaseError):
    status_code: int = 500
    error_message: str = "Error uploading."


@dataclass
class MediaFileNotFoundError(BaseError):
    status_code: int = 404
    error_message: str = "File not found."


@dataclass
class MediaFileNotAllowedExtensionError(BaseError):
    status_code: int = 415
    error_message: str = "File extension not allowed."


def media_file_exception_handler(request: Request, exc: BaseError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code,
                        content=MediaFilesResponse(error_message=exc.error_message).model_dump())


def get_responses_code(excs: list[BaseError]) -> dict[int, dict]:
    return {exc.status_code: {"model": MediaFilesResponse,
                              "description": exc.error_message} for exc in excs}


def mediafiles_register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(MediaFileUploadError, media_file_exception_handler)
    app.add_exception_handler(MediaFileNotAllowedExtensionError, media_file_exception_handler)
    app.add_exception_handler(MediaFileNotFoundError, media_file_exception_handler)
