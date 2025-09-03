### Documentação tecnica APP Unigrande

# para configurar o docker compose rode
docker compose up -d --build

# caso de erro de permissão no uso do entrypoint do banco de dados rode
cd backendunigrande 

# depois modifique a permissão do arquivo
chmod +x entrypoint.sh

### Para rodar o padrão de qualidade código

docker-compose exec backendunigrande /bin/bash

# name: Run bandit
   black .
# name: Run isort
   isort .
# name: Run isort check
   isort . --check-only
# name: Run flake8
   flake8 .

### Para rodar testes execute o seguinte comando

docker compose exec backendunigrande pytest -v

# configurando o migrations com docker
   docker-compose exec backendunigrande aerich init -t app.config.db.TORTOISE_ORM
   docker-compose exec backendunigrande aerich init-db

# configurando o migrations manualmente

# primeiro coloque o usuário unigrande_user como owner do banco pois ele estará como postgres
   sudo -u postgres psql
   ALTER DATABASE unigrande_db OWNER TO unigrande_user;
   \l

# acessar o container 
  docker-compose exec backendunigrande /bin/bash
# ative o ambiente virtual
   source venv/bin/activate
# Execute o comando para inicializar o aerich no ambiente
   aerich init -t app.config.db.TORTOISE_ORM
# Crie as tabelas e aplique as migrações já existentes:
   aerich init-db
# Se precisar gerar novas migrações após alterar seus modelos
   aerich migrate
# Execute o comando abaixo para inspecionar o SQL gerado pelo Aerich
   docker-compose exec backendunigrande aerich upgrade --dry-run
# Para aplicar as migrações no banco de dados
   aerich upgrade


# status code de uso padrão
HTTP_100_CONTINUE
HTTP_101_SWITCHING_PROTOCOLS
HTTP_200_OK
HTTP_201_CREATED
HTTP_202_ACCEPTED
HTTP_203_NON_AUTHORITATIVE_INFORMATION
HTTP_204_NO_CONTENT
HTTP_205_RESET_CONTENT
HTTP_206_PARTIAL_CONTENT
HTTP_300_MULTIPLE_CHOICES
HTTP_301_MOVED_PERMANENTLY
HTTP_302_FOUND
HTTP_303_SEE_OTHER
HTTP_304_NOT_MODIFIED
HTTP_307_TEMPORARY_REDIRECT
HTTP_308_PERMANENT_REDIRECT
HTTP_400_BAD_REQUEST
HTTP_401_UNAUTHORIZED
HTTP_402_PAYMENT_REQUIRED
HTTP_403_FORBIDDEN
HTTP_404_NOT_FOUND
HTTP_405_METHOD_NOT_ALLOWED
HTTP_406_NOT_ACCEPTABLE
HTTP_407_PROXY_AUTHENTICATION_REQUIRED
HTTP_408_REQUEST_TIMEOUT
HTTP_409_CONFLICT
HTTP_410_GONE
HTTP_411_LENGTH_REQUIRED
HTTP_412_PRECONDITION_FAILED
HTTP_413_PAYLOAD_TOO_LARGE
HTTP_414_URI_TOO_LONG
HTTP_415_UNSUPPORTED_MEDIA_TYPE
HTTP_416_RANGE_NOT_SATISFIABLE
HTTP_417_EXPECTATION_FAILED
HTTP_422_UNPROCESSABLE_ENTITY
HTTP_423_LOCKED
HTTP_424_FAILED_DEPENDENCY
HTTP_426_UPGRADE_REQUIRED
HTTP_428_PRECONDITION_REQUIRED
HTTP_429_TOO_MANY_REQUESTS
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
HTTP_500_INTERNAL_SERVER_ERROR
HTTP_501_NOT_IMPLEMENTED
HTTP_502_BAD_GATEWAY
HTTP_503_SERVICE_UNAVAILABLE
HTTP_504_GATEWAY_TIMEOUT
HTTP_505_HTTP_VERSION_NOT_SUPPORTED
HTTP_507_INSUFFICIENT_STORAGE
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED