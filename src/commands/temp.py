# Файл для теста чтобы не поднимать два сервиса
import datetime
import os

import aiofiles
import websockets
from asgiref.sync import async_to_sync

from mediafiles.config import mediafiles_logger
from mediafiles.schemas import MediaFile


class CloudClient:
    """Пример клиент для отправки файлов в облако."""
    def __init__(self) -> None:
        self.cloud_url: str = "ws://0.0.0.0:777/mediafiles/upload/ws"

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

client = CloudClient()
files = [MediaFile(
        uid=1,
        size=123456,
        format='image/jpeg',
        original_name='Q0g0lQcL66pX_f_djMwW5a3BtKSeVbzajBV-6UPpIblIY-yYKZ_1ZS8PwSYdqsKf05PnrobHwQ7ge3L7TFfVUCBl.jpg',
        extension='.jpg',
        datetime_upload=datetime.datetime.now(),
        path='/media_files_upload/media/2024-08-19T12:24:28+0000_Q0g0lQcL66pX_f_djMwW5a3BtKSeVbzajBV-6UPpIblIY-yYKZ_1ZS8PwSYdqsKf05PnrobHwQ7ge3L7TFfVUCBl.jpg',
)]
async_to_sync(client.upload_files)(files)
