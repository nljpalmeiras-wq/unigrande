#!/bin/sh

echo "Waiting for PostgreSQL..."

# Aguarde até que o banco de dados esteja acessível
while ! nc -z dbunigrande 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

# Execute o comando principal (como iniciar o servidor)
exec "$@"