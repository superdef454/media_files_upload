import argparse
import os
from datetime import datetime, timedelta

from mediafiles.config import mediafiles_logger, mediafiles_settings


def delete_old_files(days_old: int) -> None:
    cutoff_date = datetime.now() - timedelta(days=days_old)

    for filename in os.listdir(mediafiles_settings.PATH_TO_SAVE):
        file_path = os.path.join(mediafiles_settings.PATH_TO_SAVE, filename)
        if os.path.isfile(file_path):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mtime < cutoff_date:
                try:
                    os.remove(file_path)
                    mediafiles_logger.info(f"File delete: {file_path}")
                except Exception as e:
                    mediafiles_logger.error(f"Error while deleting {file_path}: {e}")
    # Следовало бы проверить все файлы из базы, есть ли они в директории, если нет, то удалить
    # И если с момента последнего изменения прошло больше количества переданных дней, то удалить и очистить из базы запись с этим файлом
    # Но не успеваю

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Удаление старых файлов из директории.")
    parser.add_argument("days", type=int, help="Количество дней для определения старых файлов.")

    args = parser.parse_args()

    delete_old_files(args.days)
