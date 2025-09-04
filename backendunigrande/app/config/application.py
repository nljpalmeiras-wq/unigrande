# app/config/application.py

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.routes import api_router
from app.auth.utils import setup_logger
from app.config.db import init_db, test_connection
from app.config.settings import ALLOWED_ORIGINS, OPENAPI_SCHEMA

logger = setup_logger()
ALLOWED_HOSTS = [
    "api.unigrande.app.br",
    "localhost",
    "127.0.0.1",
    "backendunigrande",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")

    if await test_connection():
        logger.info(
            "Conexão com o banco de dados bem-sucedida. Inicializando o banco..."
        )
        init_db(app)
    else:
        logger.error(
            "Falha ao conectar com o banco de dados. Não será possível inicializar o banco."
        )

    yield

    logger.info("Shutting down...")


def create_application() -> FastAPI:
    app = FastAPI(openapi_schema=OPENAPI_SCHEMA, lifespan=lifespan)

    # Limiter
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted Host
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)

    # Rotas
    app.include_router(api_router)

    # Rota de teste
    @app.get("/")
    def read_root():
        return {"Hello": "API está ativa no ambiente;"}

    return app
