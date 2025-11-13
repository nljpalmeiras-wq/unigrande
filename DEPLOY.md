# **DEPLOY COMPLETO DA API NA VPS**

Este guia cobre **tudo**, na ordem exata necessária para implantar sua API em produção.

senha da vps: @3Unigrande
---

# ACESSO SSH À VPS (COM CHAVE)

## 1.1 Acessar a VPS

No seu computador:

```bash
ssh root@vps62676.publiccloud.com.br
```

---

## 1.2 Configurar acesso seguro (chave pública)

### No seu computador:

```bash
cat ~/.ssh/id_rsa.pub
```

### Na VPS:

```bash
echo "SUA_CHAVE_PUBLICA_AQUI" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Agora você consegue logar **sem senha**.

---

# CRIAÇÃO DO USUÁRIO PARA DEPLOY (`github`)

```bash
adduser github
usermod -aG sudo github
```

Entrar com o novo usuário:

```bash
su - github
```

Testar permissão:

```bash
sudo whoami
```

Se retornar `root`, está OK.

---

# SEGURANÇA DO SSH

Editar config:

```bash
sudo nano /etc/ssh/sshd_config
```

Modificar:

```
PermitRootLogin no
PasswordAuthentication no
```

Reiniciar:

```bash
sudo systemctl restart ssh
```

Agora **somente o usuário github com chave SSH acessa a VPS**.

---

# FIREWALL (UFW)

Instalar:

```bash
sudo apt install ufw -y
```

Regras:

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
# Opcional
sudo ufw allow 8080/tcp
```

Padrões:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

Ativar:

```bash
sudo ufw enable
sudo ufw status verbose
```

A porta **5000 NÃO deve ser liberada**, pois é interna (Apache → Gunicorn).

---

# PREPARAR PASTA DO PROJETO

```bash
cd /var/www
sudo mkdir unigrande
sudo chown github:github unigrande
cd unigrande
```

---

# CLONAR O REPOSITÓRIO DO GITHUB

### Criar chave SSH para acessar repositório privado

-- sudo apt install git

```bash
ssh-keygen -t ed25519 -C "github@vps"
cat ~/.ssh/id_ed25519.pub
```

Adicionar a chave no GitHub → Settings > SSH Keys.

### Clonar:

```bash
git clone git@github.com:seuusuario/unigrande.git
```

Estrutura:

```
/var/www/unigrande/
 └── backendunigrande/
```

---

# CONFIGURAÇÃO DO AMBIENTE PYTHON

Dependências:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip python3-dev build-essential libpq-dev
```


## **1. Configuração do PostgreSQL**

1. **Instalar PostgreSQL:**

   ```bash
   sudo apt update
   sudo apt install -y postgresql postgresql-contrib
   ```

2. **Configurar o banco de dados:**

   - Acessar o PostgreSQL:
     ```bash
     sudo -u postgres psql
     ```

   - Criar um banco de dados e um usuário:
     ```sql
         CREATE DATABASE unigrande_db;
         CREATE USER unigrande_user WITH PASSWORD 'unigrande';
         ALTER ROLE unigrande_user SET client_encoding TO 'utf8';
         ALTER ROLE unigrande_user SET default_transaction_isolation TO 'read committed';
         ALTER ROLE unigrande_user SET timezone TO 'UTC';
         GRANT ALL PRIVILEGES ON DATABASE unigrande_db TO unigrande_user;
     ```



3. **Verificar o status do PostgreSQL:**

   ```bash
   sudo systemctl status postgresql
   ```

Criar e ativar venv:

```bash
cd /var/www/unigrande/backendunigrande
python3 -m venv venv
source venv/bin/activate
```

Instalar libs:

```bash
pip install -U pip wheel
pip install -r requirements.txt
pip install python-dotenv
```


   # para acessar o postgresql
   psql -U unigrande_user -d unigrande_db -h 127.0.0.1 -p 5432

   # para ajustar configurações do postgresql
   sudo nano /etc/postgresql/15/main/postgresql.conf
   sudo nano /var/log/postgresql/postgresql-15-main.log

   CREATE USER unigrande_user WITH PASSWORD '9b4H3E';

   # acessar o container 
   docker-compose exec backendsergipanidade /bin/bash

   # configurando o migrations com docker
   docker-compose exec backendsergipanidade aerich init -t app.config.db.TORTOISE_ORM
   docker-compose exec backendsergipanidade aerich init-db

   # configurando o migrations manualmente

   # primeiro coloque o usuário unigrande_user como owner do banco pois ele estará como postgres
   sudo -u postgres psql
   ALTER DATABASE unigrande_db OWNER TO unigrande_user;
   \l

   # ative o ambiente virtual
   source venv/bin/activate
   # Execute o comando para inicializar o aerich no ambiente
   aerich init -t app.config.db.TORTOISE_ORM
   # Crie as tabelas e aplique as migrações já existentes:
   aerich init-db
   # Se precisar gerar novas migrações após alterar seus modelos
   aerich migrate
   # Execute o comando abaixo para inspecionar o SQL gerado pelo Aerich
   docker-compose exec backend aerich upgrade --dry-run
   # Para aplicar as migrações no banco de dados
   aerich upgrade

   # para deletar as tabelas no postgresql, entre com o usário dentro do bd
   # Desativar temporariamente as restrições de chave estrangeira
   SET session_replication_role = replica;

   # Gerar os comandos para deletar todas as tabelas
   DO $$ DECLARE
    tbl RECORD;
   BEGIN
      FOR tbl IN
         SELECT tablename
         FROM pg_tables
         WHERE schemaname = 'public'
      LOOP
         EXECUTE FORMAT('DROP TABLE IF EXISTS %I CASCADE', tbl.tablename);
      END LOOP;
   END $$;

   # Reativar as restrições de chave estrangeira
   SET session_replication_role = DEFAULT;

---

# CONFIGURAR ARQUIVO `.env`

Criar:

```bash
nano .env
```

Exemplo:

```env
ENVIRONMENT=production
DATABASE_URL=postgres://unigrande_user:senha@127.0.0.1:5432/unigrande_db
ALLOWED_ORIGINS=*
ALLOWED_HOSTS=vps62676.publiccloud.com.br,localhost,127.0.0.1
BASE_URL=https://vps62676.publiccloud.com.br
SECRET_KEY=SUPER-SECRETA
```

---

# TESTAR API MANUALMENTE

```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

Testar:

```bash
curl http://127.0.0.1:5000
```

---

# CONFIGURAR GUNICORN (SYSTEMD)

Criar arquivo:

```bash
sudo nano /etc/systemd/system/fastapi.service
```

Conteúdo:

```ini
[Unit]
Description=FastAPI application
After=network.target

[Service]
User=github
WorkingDirectory=/var/www/unigrande/backendunigrande
Environment="PATH=/var/www/unigrande/backendunigrande/venv/bin"
ExecStart=/var/www/unigrande/backendunigrande/venv/bin/gunicorn \
  -w 1 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:5000 \
  --timeout 1800 --graceful-timeout 1800 \
  app.main:app

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Ativar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl start fastapi
sudo systemctl status fastapi
```

---

# APACHE COMO PROXY REVERSO

Instalar módulos:

```bash
sudo apt update
sudo apt install -y apache2
sudo a2enmod proxy proxy_http ssl headers rewrite
```

Criar conf HTTP:

```bash
sudo nano /etc/apache2/sites-available/fastapi.conf
```

```apache
<VirtualHost *:80>
    ServerName vps62676.publiccloud.com.br

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/

    RewriteEngine On
    RewriteCond %{HTTPS} !=on
    RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]

    ErrorLog ${APACHE_LOG_DIR}/fastapi_error.log
    CustomLog ${APACHE_LOG_DIR}/fastapi_access.log combined
</VirtualHost>
```

Ativar:

```bash
sudo a2ensite fastapi.conf
sudo systemctl reload apache2
```

---

# SSL VIA CERTBOT (HTTPS)

```bash
sudo apt install certbot python3-certbot-apache -y
sudo certbot --apache -d vps62676.publiccloud.com.br
```

Ajustar timeouts para uploads grandes:

```bash
sudo nano /etc/apache2/sites-enabled/fastapi-le-ssl.conf
```

Adicionar dentro do VirtualHost:

```apache
ProxyTimeout 1200
RequestReadTimeout header=600-1200 body=600-1200
TimeOut 1200
```

Recarregar:

```bash
sudo systemctl reload apache2
```

---

# AJUSTAR PERMISSÕES

```bash
sudo chown -R github:www-data /var/www/unigrande
sudo chmod -R 755 /var/www/unigrande
```