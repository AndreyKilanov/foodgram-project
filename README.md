# Проект Foodgram

Foodgram - веб-приложение которое хранит в себе базу рецептов, ингредиентов. Имеет свою полноценную API. Есть своя админка.
Есть авторизация, регистрация, смена пароля, возможность получения/удаления токена для API.

У пользователей есть возможность создавать, редактировать и удалять рецепты. Не авторизованные пользователи могут просматривать рецепты.
Так же пользователи могут добавлять рецепты в избранное, подписываться на других авторов, просматривать их рецепты.

Есть возможность добавлять рецепты в список покупок, где можно скачать список ингредиентов в формате txt.


## Используемые технологии

Python, Django, Django Rest Framework, Docker, Gunicorn, NGINX, PostgreSQL, Yandex Cloud.

## Проект доступен по адресу:

<http://84.252.143.127>

## Как запустить проект

>*Клонировать репозиторий и перейти в него в командной строке:*

* ```bash
    git@github.com:AndyFebruary74/foodgram-project-react.git
  ```

* ```bash
  cd foodgram-project-react/
  ```

>*Запустить docker-compose и собрать образы:*

* ```bash
  cd infra/
  ```

* ```bash
  docker-compose up -d --build
  ```

>*Выполнить миграции, создать суперюзера, собрать статику и импортировать список ингредентов:*

* ```bash
  docker-compose exec backend python manage.py migrate
  docker-compose exec backend python manage.py createsuperuser
  docker-compose exec backend python manage.py collectstatic --no-input
  docker-compose exec backend python manage.py load_csv
  ```

* >*Теперь проект доступен по адресу <http://84.252.143.127>*
* >*Админка доступна по адресу <http://84.252.143.127/admin>*
* >*Документация к API доступна по адресу <http://84.252.143.127/api/docs/redoc.html>*

>*Пример заполнения .env файла (должен находиться по адресу foodgram-project-react/infra/):*

```python
    # Django Secret Key
    
    DJANGO_SECRET_KEY = 'DJANGO_SECRET_KEY' # Секретный ключ
    
    # Debug Settings
    
    DEBUG = False # Default False
    
    # Settings Postgres
    
    DB_ENGINE=django.db.backends.postgresql # указываем БД postgresql
    DB_NAME=postgres_db # имя базы данных
    POSTGRES_USER=postgres # логин для подключения к базе данных
    POSTGRES_PASSWORD=postgres # пароль для подключения к БД
    DB_HOST=db # название контейнера
    DB_PORT=5432 # порт для подключения к БД
```

>*Пример создания БД в контейнере postgres:*

```SQL
    docker exec -it <CONTAINER_ID> bash
    su - postgres
    psql
    CREATE DATABASE <NAME_DB>;
    CREATE USER <USERNAME> WITH ENCRYPTED PASSWORD 'PASSWORD';
    GRANT ALL PRIVILEGES ON DATABASE <NAME_DB> TO <USERNAME>;
    \l
```

## Примеры работы с API

### POST запрос. Регистрация нового пользователя

```URL
http://84.252.143.127/api/users/
```

>*request:*

* ```JSON
    {
        "email": "vpupkin@yandex.ru",
        "username": "vasya.pupkin",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "password": "Qwerty123"
    }
  ```

>*response:*

* ```JSON
    {
        "email": "vpupkin@yandex.ru",
        "id": 0,
        "username": "vasya.pupkin",
        "first_name": "Вася",
        "last_name": "Пупкин"
    }
  ```

### POST запрос. Получения токена авторизации

```URL
http://84.252.143.127/api/auth/token/login/
```

>*request:*

* ```JSON
    {
        "password": "string",
        "email": "string"
    }
  ```

>*response:*

* ```JSON
    {
        "auth_token": "string"
    }
  ```

### GET запрос. Получение списка рецептов

```URL
http://84.252.143.127/api/recipes/
```

* ```JSON
    {
      "count": 123,
      "next": "http://foodgram.example.org/api/recipes/?page=4",
      "previous": "http://foodgram.example.org/api/recipes/?page=2",
      "results": [
        {
          "id": 0,
          "tags": [
            {
              "id": 0,
              "name": "Завтрак",
              "color": "#E26C2D",
              "slug": "breakfast"
            }
          ],
          "author": {
            "email": "user@example.com",
            "id": 0,
            "username": "string",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "is_subscribed": false
          },
          "ingredients": [
            {
              "id": 0,
              "name": "Картофель отварной",
              "measurement_unit": "г",
              "amount": 1
            }
          ],
          "is_favorited": true,
          "is_in_shopping_cart": true,
          "name": "string",
          "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
          "text": "string",
          "cooking_time": 1
        }
      ]
    }
  ```
