FROM php:8-cli

WORKDIR /srv/frontend
COPY frontend/ /srv/frontend/
COPY backend/ /srv/backend/

EXPOSE 8000

CMD ["php", "-S", "0.0.0.0:8000", "../backend/server.php"]
