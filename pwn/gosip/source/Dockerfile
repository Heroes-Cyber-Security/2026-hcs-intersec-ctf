FROM debian:trixie@sha256:9cc080028c43b27d2074d63a5f9caf7166d731494965616c1a6d2827a004585c

RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m gosip
WORKDIR /home/gosip

COPY chall /home/gosip/chall
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /home/gosip/chall && \
    chmod +x /entrypoint.sh && \
    chown root:root /home/gosip && \
    chmod 755 /home/gosip && \
    chown gosip:gosip /home/gosip

USER gosip
EXPOSE 4412

ENTRYPOINT ["/entrypoint.sh"]
