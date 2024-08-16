from mediafiles import service
from mediafiles.exceptions import MediaFileNotFoundError
from mediafiles.schemas import MediaFile


async def valid_mediafile_uid(mediafile_uid: int) -> MediaFile:
    mediafile = await service.MediaFileService.get_by_uid(mediafile_uid)
    if not mediafile:
        raise MediaFileNotFoundError
    return mediafile
