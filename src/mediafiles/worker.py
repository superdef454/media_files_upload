from asgiref.sync import async_to_sync
from celery import Celery

from config import settings
from mediafiles.cloud_client import CloudClient

celery = Celery(
    "media_files_upload",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
   )

celery.conf.update(
       task_serializer="json",
       accept_content=["json"],
       result_serializer="json",
       timezone="UTC",
       enable_utc=True,
   )

@celery.task
def process_cloud_uploaded(file_paths: list[str]):
    cloud_client = CloudClient()
    async_to_sync(cloud_client.upload_files)(file_paths)
