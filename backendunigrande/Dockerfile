# Pull official base image for Python 3.11.2 and Debian 12 (bookworm)
FROM python:3.11.2-slim

# Crie um usuário não-root (se já não existir)
RUN useradd -m elisrenan

# Set working directory
WORKDIR /usr/src/app

# Instale dependências do sistema enquanto é root
USER root

RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies
RUN pip install --upgrade pip

# Copy and install python dependencies from requirements.txt
COPY ./requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# Altere o dono do diretório para o novo usuário
RUN chown -R elisrenan:elisrenan /usr/src/app

# Defina o usuário no Dockerfile para a execução da aplicação
USER elisrenan

# Run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
