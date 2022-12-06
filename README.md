# Дипломный проект Foodgram
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/downloads/release/python-379/) [![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/) [![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/) [![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/) [![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/) [![Workflow](https://github.com/Rezenhorn/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/Rezenhorn/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

## Описание:
- Проект Foodgram "Продуктовый помощник" является сайтом для публикации рецептов. Пользователь может публиковать свои рецепты, подписываться на других авторов, добавлять рецепты в избранное, а также добавлять рецепты в список покупок и скачивать файл с необходимыми ингредиентами и их количеством. У каждого рецепта есть теги, время приготовления, ингредиенты с количеством, описание и картинка.
Проект запущен по адресу: http://158.160.20.159/
Данные для входа в админ-панель:
- Email: admin@admin.ru
- Пароль: admin

## Как запустить проект локально:
### Клонировать репозиторий и перейти в него:
```
git clone https://github.com/Rezenhorn/foodgram-project-react.git
```
### Создать файл .env в папке backend/ и заполнить его в соответствии с примером (файл .env.example):
### Убедиться, что на компьютере установлен Docker
### Из папки infra/ запустить Docker:
```
docker-compose up -d --build
```
### Выполнить миграции, создать суперпользователя, собрать статику:
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
```
## Чтобы прекратить работу, необходимо остановить собранные контейнеры:
```
docker-compose down -v
```