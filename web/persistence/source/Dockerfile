FROM php:8.2-apache

RUN apt-get update && apt-get install -y --no-install-recommends xxd \
    && rm -rf /var/lib/apt/lists/*

RUN a2enmod rewrite

RUN mkdir -p /var/www/uploads \
    && chown www-data:www-data /var/www/uploads \
    && chmod 750 /var/www/uploads

RUN printf 'session.upload_progress.enabled = On\nsession.upload_progress.cleanup = Off\n' \
    > /usr/local/etc/php/conf.d/zz-vaultnotes.ini

RUN echo "How could you :P" > /usr/local/lib/php/pearcmd.php

COPY html/ /var/www/html/
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 80

CMD ["/usr/local/bin/entrypoint.sh"]
