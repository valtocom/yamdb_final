# Запуск docker-compose. Проект YaMDb

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

Яндекс Практикум. Спринт 15. Запуск docker-compose

## Описание

Проект `YaMDb` собирает отзывы пользователей на произведения из категорий: «Книги», «Фильмы», «Музыка».

## Функционал

- Произведения делятся на категории. Список категорий может быть расширен администратором;
- Произведения, фильмы и музыка не хранятся в приложении;
- В каждой категории есть произведения: книги, фильмы или музыка;
- Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор;
- Пользователи могут оставлять отзывы и ставить оценку произведениям. Из пользовательских оценок формируется рейтинг. На одно произведение можно оставить только один отзыв.

## Установка

1. Проверить наличие Docker

   Прежде чем приступать к работе, убедиться что Docker установлен, для этого ввести команду:

   ```bash
   docker -v
   ```

   В случае отсутствия, скачать [Docker Desktop](https://www.docker.com/products/docker-desktop) для Mac или Windows. [Docker Compose](https://docs.docker.com/compose) будет установлен автоматически.

   В Linux проверить, что установлена последняя версия [Compose](https://docs.docker.com/compose/install/).

   Также можно воспользоваться официальной [инструкцией](https://docs.docker.com/engine/install/).

2. Клонировать репозиторий на локальный компьютер

   ```bash
   git clone https://github.com/valtocom/infra_sp2.git
   ```

3. В корневой директории создать файл `.env`, согласно примеру:

   ```bash
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432
   ```

4. Запустить `docker-compose`

   Выполнить из корневой директории команду:

   ```bash
   docker container run --detach
   ```

5. Заполнить базу данных

   Создать и выполнить миграции:

   ```bash
   docker-compose exec web python manage.py makemigrations --noinput
   docker-compose exec web python manage.py migrate --noinput
   ```

6. Подгрузить статику

   ```bash
   docker-compose exec web python manage.py collectstatic --no-input
   ```

7. Заполнить БД тестовыми данными

   Для заполнения базы использовать файл `fixtures.json`, в директории `infra_sp2`. Выполните команду:

   ```bash
   docker-compose exec web python manage.py dumpdata > fixtures.json
   ```

8. Создать суперпользователя

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

9. Остановить работу всех контейнеров

   ```bash
   docker-compose down -v
   ```

10. Пересобрать и запустить контейнеры

    ```bash
    docker-compose up -d --build
    ```

11. Мониторинг запущенных контейнеров

    ```bash
    docker stats
    ```

12. Остановить и удалить контейнеры, тома и образы

    ```bash
    docker-compose down -v
    ```
