Горные перевалы!

Здесь вы можете получить или добавить информацию
о горных перевалах и их сложности в зависимости от врменени года.
 Турист поднимется на перевал,
он сфотографирует его и внесёт нужную информацию с помощью 
мобильного приложения:

- координаты объекта и его высоту;
- название объекта;
- несколько фотографий;
- информацию о пользователе, который передал данные о перевале:
- имя пользователя (ФИО строкой);
- почта;
- телефон.

Для установки потребуются следующие зависимости:
- alembic==1.11.1
- anyio==3.7.0
- click==8.1.3
- colorama==0.4.6
- fastapi==0.95.2
- greenlet==2.0.2
- h11==0.14.0
- idna==3.4
- Mako==1.2.4
- MarkupSafe==2.1.2
- pydantic==1.10.8
- python-dotenv==1.0.0
- sniffio==1.3.0
- SQLAlchemy==2.0.15
- starlette==0.27.0
- typing_extensions==4.6.2
- uvicorn==0.22.0

Ниже приведены описания методов:


Создание новой записи перевала.
Этот метод позволяет создать новую запись перевала.

HTTP-метод: POST
URL: /submitData
Параметры запроса: JSON-объект с данными перевала (pereval)
import requests

data = {
    "pereval": {
        "beauty_title": "Новый заголовок",
        "title": "Новый заголовок",
        "other_titles": "Новые заголовки",
        "connect": "Новое подключение",
        "add_time": "2021-09-22T13:18:13",
        "status": "new",
        "coords": {
            "latitude": 50.12345,
            "longitude": 30.6789,
            "height": 100
        },
        "level": {
            "winter": "Сложный",
            "summer": "Средний",
            "autumn": "Простой",
            "spring": "Средний"
        },
        "images": [
            {
                "image_name": "Новое изображение 3",
                "title": "Новый заголовок 3"
            },
            {
                "image_name": "Новое изображение 4",
                "title": "Новый заголовок 4"
            }
        ]
    }
}

response = requests.post("http://localhost:8000/submitData", json=data)
result = response.json()
print(result)


Получение данных о перевале по ID.
Этот метод позволяет получить данные о перевале по его ID.

HTTP-метод: GET
URL: /submitData/{id}
Параметры запроса: ID перевала (id)

import requests

id = 1
response = requests.get(f"http://localhost:8000/submitData/{id}")
result = response.json()
print(result)


Обновление данных перевала.
Этот метод позволяет обновить данные о перевале.

HTTP-метод: PATCH
URL: /submitData/{id}
Параметры запроса: ID перевала (id), JSON-объект с обновленными данными перевала (data)

import requests

id = 1
data = {
    "beauty_title": "Новый заголовок",
    "title": "Новый заголовок",
    "other_titles": "Новые заголовки",
    "connect": "Новое подключение",
    "coords": {
        "latitude": 50.12345,
        "longitude": 30.6789,
        "height": 100
    },
    "level": {
        "winter": "Сложный",
        "summer": "Средний",
        "autumn": "Простой",
        "spring": "Средний"
    },
    "images": [
        {
            "image_name": "Новое изображение 3",
            "title": "Новый заголовок 3"
        },
        {
            "image_name": "Новое изображение 4",
            "title": "Новый заголовок 4"
        }
    ]
}

response = requests.patch(f"http://localhost:8000/submitData/{id}", json=data)
result = response.json()
print(result)


Получение данных перевала по эл.почте пользователя.
Этот метод позволяет получить данные о перевале пользователя по его email-адресу.

HTTP-метод: GET
URL: /submitData/
Параметры запроса: email пользователя (user__email)
Пример использования (Python):
python
Copy code
import requests

email = "example@example.com"  # Замените на нужный email пользователя
params = {"user__email": email}
response = requests.get("http://localhost:8000/submitData", params=params)
data = response.json()
print(data)