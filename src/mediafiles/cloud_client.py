import asyncio
import os

import aiofiles
import aiohttp

from mediafiles.config import mediafiles_logger, mediafiles_settings


class CloudClient:
    """Пример клиент для отправки файлов в облако."""
    def __init__(self) -> None:
        self.cloud_url: str = mediafiles_settings.CLOUD_URL

    async def upload_file(self, file_path: str) -> dict | None:
        if not self.cloud_url:  # Проверка настройки облака
            return None
        if not os.path.exists(file_path):  # Проверка на существование файла
            await mediafiles_logger.error(f"File not found: {file_path}")
            return None
        async with aiohttp.ClientSession() as session, aiofiles.open(file_path, "rb") as file:
            async def file_stream():  # Загружаем файл частями
                    chunk_size = 1024 * 1024
                    while True:
                        chunk = await file.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk
            data = aiohttp.AsyncIterablePayload(file_stream())
            try:
                async with session.post(self.cloud_url, data=data) as response:
                    response_data = await response.json()
                    if not response.ok:
                        await mediafiles_logger.error(
                            f"Failed to upload file: {file_path}. "
                            f"Status: {response.status}, Response: {response_data}",
                        )
                    else:
                        await mediafiles_logger.info(f"File uploaded successfully: {file_path}")
                        return response_data
            except aiohttp.ClientError as e:
                await mediafiles_logger.error(f"HTTP error occurred: {e}")
        return None

    async def upload_files(self, file_paths: list[str]):
        tasks = [asyncio.create_task(self.upload_file(file_path)) for file_path in file_paths]
        return await asyncio.gather(*tasks)
