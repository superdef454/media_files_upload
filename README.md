# media_files_upload

## Работа с окружением

### Dev

poetry install  `Установить зависимости проекта`

poetry add "package==1.2.3"  `Добавить новую библиотеку`
poetry add --dev package==1.2.3  `Добавить --dev зависимость`

poetry remove fastapi  `Удалить зависимость`

poetry lock --no-update  `Обновляем лок`

poetry export --without-hashes -f requirements.txt > requirements.txt  `Сделать requirements.txt для прода`  <!-- # TODO Собрать файл в конце -->
<!-- poetry export --without-hashes --with dev -f requirements.txt > requirements-dev.txt  `Сделать requirements-dev.txt для разработки` -->

### Prod

Установить зависимости из requirements.txt
