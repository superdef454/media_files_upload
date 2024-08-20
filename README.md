# media_files_upload

## Работа с окружением

### Dev

poetry install  `Установить зависимости проекта`

poetry add "package==1.2.3"  `Добавить новую библиотеку`
poetry add --dev package==1.2.3  `Добавить --dev зависимость`

poetry remove fastapi  `Удалить зависимость`

poetry lock --no-update  `Обновляем лок`

poetry export --without-hashes -f requirements.txt > requirements.txt  `Сделать requirements.txt для прода в папку src`  <!-- # TODO Собрать файл в конце -->

### Prod

Установить зависимости из requirements.txt

## Запуск проекта

### Docker

docker compose -f "docker-compose.yml" up -d --build

После запуска проект будет располагаться здесь ([Документация](http://0.0.0.0:777/docs#/))

