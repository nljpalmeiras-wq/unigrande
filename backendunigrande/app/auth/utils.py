import logging
import os
from datetime import datetime, timedelta, timezone
from logging.handlers import TimedRotatingFileHandler

from jose import jwt

from app.config.settings import ALGORITHM, EXPIRES_MINUTES, SECRET_KEY


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(EXPIRES_MINUTES)
):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def cleanup_old_logs(log_directory: str, keep_last_days: int = 10):
    """
    Remove os arquivos de log mais antigos com extensão .txt, mantendo apenas os últimos N dias.
    """
    # Lista todos os arquivos .txt no diretório de logs
    log_files = [
        os.path.join(log_directory, f)
        for f in os.listdir(log_directory)
        if os.path.isfile(os.path.join(log_directory, f))
        and f.startswith("log_")
        and f.endswith(".txt")  # Filtra apenas arquivos .txt
    ]

    # Ordena os arquivos pela data de criação (mais antigos primeiro)
    log_files.sort(key=os.path.getctime)

    # Remove arquivos mais antigos se houver mais do que os especificados
    while len(log_files) > keep_last_days:
        os.remove(log_files.pop(0))  # Remove o mais antigo


def setup_logger():
    # Diretório para os logs
    log_directory = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_directory, exist_ok=True)

    # Chamada para limpar os logs antigos
    cleanup_old_logs(log_directory, keep_last_days=10)

    # Configuração do logger personalizado
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.INFO)

    # Nome do arquivo de log com data no formato log_dd_mm_yyyy.txt
    current_date = datetime.now().strftime("%d_%m_%Y")
    log_file = os.path.join(
        log_directory, f"log_{current_date}.txt"
    )  # Nome do arquivo com a data

    handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=7
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # Configuração do logger do Uvicorn
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.DEBUG)

    # Garantir que os handlers não sejam adicionados múltiplas vezes
    if not uvicorn_logger.handlers:
        uvicorn_handler = (
            logging.StreamHandler()
        )  # Usar StreamHandler ou um outro tipo de handler
        uvicorn_handler.setFormatter(formatter)
        uvicorn_logger.addHandler(uvicorn_handler)

    return logger
