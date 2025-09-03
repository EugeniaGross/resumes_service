# Микросервис резюме пользователей
###### Подготовка сервиса к запуску
В корневой папке проекта создать файл .env. Пример содержания .env:</br>
```
JWT_ALGORITHM = "RS256"
AUTH_SERVICE_URL = http://auth_api
PUBLIC_KEY_PATH = /api/v1/jwt.key

ALLOWED_HOSTS_STRING=localhost,127.0.0.1
ORIGINS_STRING=http://localhost:5173

TEST_ALLOWED_HOSTS_STRING=test
TEST_ORIGINS_STRING=http://test

POSTGRES_PORT=5432
POSTGRES_DB=resumes
POSTGRES_USER=resumes
POSTGRES_PASSWORD=12345678
POSTGRES_HOST=db

TESTING = 1 # указывается при проведении тестирования
```

###### Запуск сервиса c помошью docker compose: </br>
```
docker compose up --build
```
###### Запуск сервиса без docker compose (Windows): </br>
```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
alembic upgrade head
cd application
uvicorn main:app --reload
```
###### Запуск сервиса без docker compose (Linux, MacOS): </br>
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
cd application
uvicorn main:app --reload
```
###### Для запуска всех сервисов и фронтенда вместе: </br>
Для запуска на одном сервере можно склонировать репозитории в одну папку.
В эту папку добавить файл docker-compose.yaml c содержанием из файла docker-compose.example.yaml
Сервис аутентификации: https://github.com/EugeniaGross/auth_service
Frontend: https://github.com/EugeniaGross/frontend_resumes_project
