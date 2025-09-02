import pytest_asyncio
from httpx import AsyncClient
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel

from application.main import app
from application.database import async_engine


class FakeAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.headers.get("Authorization") is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Доступ запрещен"},
            )
        request.state.user_id = 1
        response = await call_next(request)
        return response


app.add_middleware(FakeAuthMiddleware)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """
    Фикстура для настройки тестовой базы данных.
    - Создаёт таблицы для моделей.
    - После тестов удаляет таблицы.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: SQLModel.metadata.create_all(
                bind=sync_conn, checkfirst=True
            )
        )

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: SQLModel.metadata.drop_all(bind=sync_conn, checkfirst=True)
        )


@pytest_asyncio.fixture(scope="function")
async def ac():
    """Асинхронный HTTP-клиент для тестов"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
