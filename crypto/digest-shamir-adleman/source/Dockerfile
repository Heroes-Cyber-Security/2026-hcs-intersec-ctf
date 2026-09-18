FROM python:3.12-slim

# Run as a non-root user
RUN useradd -m -u 1000 ctf
WORKDIR /app

COPY server.py .

RUN chown -R ctf:ctf /app
USER ctf

EXPOSE 5000

CMD ["python3", "-u", "server.py"]
