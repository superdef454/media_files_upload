import os

import aiofiles
import websockets

from mediafiles.config import mediafiles_logger, mediafiles_settings
from mediafiles.schemas import MediaFile


class CloudClient:
    """Пример клиент для отправки файлов в облако."""
    def __init__(self) -> None:
        self.cloud_url: str = mediafiles_settings.CLOUD_URL

    async def upload_files(self, mediafiles: list[MediaFile]):
        async with websockets.connect(self.cloud_url) as websocket:
            for mediafile in mediafiles:
                if not os.path.exists(mediafile.path):  # Проверка на существование файла
                    await mediafiles_logger.error(f"Cloud file not found: {mediafile.path}")
                    continue
                # Отправляем имя файла
                await websocket.send(mediafile.original_name)
                # Отправляем сам файл
                async with aiofiles.open(mediafile.path, 'rb') as f:
                    while chunk := await f.read(1024):
                        await websocket.send(chunk)
                # Отправляем пустой блок данных для обозначения конца файла
                await websocket.send(b'')
            # Отправляем сигнал окончания передачи файлов
            await websocket.send("END")
