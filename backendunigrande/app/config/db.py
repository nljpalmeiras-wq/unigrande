import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import RegisterTortoise

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

log = logging.getLogger("uvicorn")

# Define a URL base com base no ambiente
DATABASE_URL = os.getenv("DATABASE_URL")
 
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    """
    Função para inicializar a conexão com o banco de dados e registrar o Tortoise ORM no FastAPI.
    """
    RegisterTortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
    )


async def generate_schema() -> None:
    """
    Função assíncrona para gerar o esquema do banco de dados utilizando Tortoise.
    """
    log.info("Inicializando Tortoise...")

    try:
        # Inicializa a conexão com o banco de dados
        await Tortoise.init(
            db_url=DATABASE_URL,
            modules={"models": ["app.models.tortoise"]},
        )

        log.info("Gerando esquema do banco de dados via Tortoise...")

        # Gera as esquemas (tabelas, colunas, etc.)
        await Tortoise.generate_schemas()
    except Exception as e:
        log.error(f"Erro ao gerar o esquema do banco de dados: {e}")
    finally:
        # Fecha a conexão com o banco de dados
        await Tortoise.close_connections()


async def test_connection() -> bool:
    """
    Função para testar a conexão com o banco de dados.
    Retorna True se a conexão for bem-sucedida, caso contrário, False.
    """
    try:
        # Teste de conexão
        await Tortoise.init(
            db_url=DATABASE_URL,
            modules={"models": ["app.models.tortoise", "aerich.models"]},
        )
        log.info("Conexão bem-sucedida!")
        return True
    except Exception as e:
        log.error(f"Erro na conexão: {e}")
        return False
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    # Testa a conexão antes de realizar qualquer outra ação
    if run_async(test_connection()):
        # Se a conexão for bem-sucedida, gera o esquema do banco de dados
        run_async(generate_schema())
    else:
        log.error("Não foi possível estabelecer a conexão com o banco de dados.")
