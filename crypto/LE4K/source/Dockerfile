FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends socat && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1000 ctf
WORKDIR /app

RUN pip install --no-cache-dir pycryptodome
COPY server.py .

USER ctf

EXPOSE 5000

CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:python3 -u chall.py"]
