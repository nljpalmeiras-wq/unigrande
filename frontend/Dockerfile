# Use a imagem oficial do Debian 12
FROM debian:12

# Adicione o repositório surý para PHP 8.3
RUN apt-get update && \
    apt-get install -y lsb-release apt-transport-https ca-certificates wget && \
    wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg && \
    echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/php.list

# Atualize os pacotes e instale o Apache e PHP 8.3 com módulos necessários
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    apache2 \
    php8.3 \
    libapache2-mod-php8.3 \
    php8.3-mysql php8.3-cli php8.3-gd php8.3-curl \
    php8.3-mbstring php8.3-xml php8.3-zip unzip && \
    # Limpeza de arquivos temporários
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ativar extensões mbstring e dom no php.ini
RUN sed -i 's/;extension=mbstring/extension=mbstring/' /etc/php/8.3/apache2/php.ini && \
    sed -i 's/;extension=dom/extension=dom/' /etc/php/8.3/apache2/php.ini

# Latest release
COPY --from=composer/composer:latest-bin /composer /usr/bin/composer

# Configurar o ServerName para o Apache
RUN echo "ServerName localhost" | tee /etc/apache2/conf-available/fqdn.conf && \
    a2enconf fqdn

# Configurar o Virtual Host
RUN echo '<VirtualHost *:80>\n\
    DocumentRoot /var/www/unigrande/frontend\n\
    <Directory /var/www/unigrande/frontend>\n\
        Options Indexes FollowSymLinks\n\
        AllowOverride All\n\
        Require all granted\n\
    </Directory>\n\
</VirtualHost>' > /etc/apache2/sites-available/000-default.conf

# Copie os arquivos PHP para o diretório raiz do Apache
COPY . /var/www/unigrande/frontend

# Exponha a porta 80
EXPOSE 80

# Habilite o módulo de reescrita do Apache
RUN a2enmod rewrite

# Inicie o Apache em primeiro plano
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
