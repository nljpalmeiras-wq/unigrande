import logging
import os
from functools import lru_cache

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from pydantic import AnyUrl
from pydantic_settings import BaseSettings

# Carrega as variáveis de ambiente do arquivo .env
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
EXPIRES_MINUTES = 30
TOKEN_URL = "/users/login/admin"
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

log = logging.getLogger("uvicorn")
load_dotenv()


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = 0
    database_url: AnyUrl = None


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


# Instância do FastAPI com OpenAPI configurada
OPENAPI_SCHEMA = {
    "openapi": "3.0.2",
    "info": {
        "title": "Unigrande API",
        "version": "1.0.0",
        "description": "API Unigrande",
    },
    "components": {
        "securitySchemes": {
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": {
                    "password": {
                        "tokenUrl": "/users/login/admin",  # Este é o endpoint que gera o token
                    }
                },
            }
        }
    },
    "security": [
        {"OAuth2PasswordBearer": []}
    ],  # Garantir que todas as rotas usem esse esquema de segurança
}
