![example event parameter](https://github.com/valtocom/yamdb_final/actions/workflows/main.yml/badge.svg?event=push)

# CI и CD проекта api_yamdb

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

Яндекс Практикум. Спринт 16. CI и CD проекта api_yamdb

## Описание

Проект `YaMDb` собирает отзывы пользователей на произведения из категорий: «Книги», «Фильмы», «Музыка».

## Функционал

- Произведения делятся на категории. Список категорий может быть расширен администратором;
- Произведения, фильмы и музыка не хранятся в приложении;
- В каждой категории есть произведения: книги, фильмы или музыка;
- Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор;
- Пользователи могут оставлять отзывы и ставить оценку произведениям. Из пользовательских оценок формируется рейтинг. На одно произведение можно оставить только один отзыв.

## Установка

1. Клонировать репозиторий:

    ```python
    git clone git@github.com:valtocom/yamdb_final.git
    ```

2. Создать и активировать виртуальное пространство, установить зависимости и запустить тесты:

    Для Windows:

    ```python
    cd yamdb_final
    python -m venv venv
    source venv/Scripts/activate
    cd api_yamdb
    pip install -r requirements.txt
    cd ..
    pytest
    ```

    Для Mac/Linux:

    ```python
    cd yamdb_final
    python3 -m venv venv
    source venv/bin/activate
    cd api_yamdb
    pip install -r requirements.txt
    cd ..
    pytest
    ```

3. Запустить контейнер Docker:

    - Проверить статус Docker:

    ```python
    docker --version
    ```

    - Запустить docker-compose:

    ```python
    cd infra/
    docker-compose up -d
    ```

4. Выполнить миграции, создать суперпользователя и собрать статику:

    ```python
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    docker-compose exec web python manage.py collectstatic --no-input
    ```

5. Для запуска в виртуальном окружении, после создания и активации виртуального пространства, установки зависимостей, запустить проект локально:

    Для Windows:

    ```python
    python manage.py runserver
    ```

    Для Mac/Linux:

    ```python
    python3 manage.py runserver
    ```

6. Проверить доступность сервиса:

    ```python
    http://158.160.66.251/admin
    ```
