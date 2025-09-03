from pathlib import Path
import os
import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from history_improvements.routers import router as history_improvements_router
from resumes.routers import router as resumes_router
from settings import settings
from utils.auth_service import AuthClient
from utils.tokens import JWTTokenService

if not settings.TESTING:
    from uvicorn.workers import UvicornWorker

    class BackendUvicornWorker(UvicornWorker):
        """
        Воркер с настроенным логгированием
        """

        CONFIG_KWARGS = {
            "log_config": (
                f"{str(Path(__file__).resolve().parent.parent) + os.sep}logging.yaml"
            ),
        }


class AuthorizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path != "/api/v1/resumes/openapi.json":
            access_token = request.headers.get("Authorization")
            if not access_token or not access_token.startswith("Bearer "):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Доступ запрещен"},
                )
            try:
                auth_client = AuthClient()
                public_key = await auth_client.get_public_key()
            except RuntimeError as e:
                logging.error(e)
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"detail": "Сервис временно не доступен"},
                )
            decode_token = JWTTokenService.decode_jwt_token(
                access_token.replace("Bearer ", ""), public_key
            )
            if decode_token is None or decode_token.get("type") != "access":
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Доступ запрещен"},
                )
            request.state.user_id = decode_token.get("id")
        response = await call_next(request)
        return response


app = FastAPI(
    openapi_url="/api/v1/resumes/openapi.json"
)

if not settings.TESTING:
    app.add_middleware(AuthorizationMiddleware)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=(
        settings.ALLOWED_HOSTS if not settings.TESTING else settings.TEST_ALLOWED_HOSTS
    ),
)

origins = settings.ORIGINS if not settings.TESTING else settings.TEST_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resumes_router)
app.include_router(history_improvements_router)
