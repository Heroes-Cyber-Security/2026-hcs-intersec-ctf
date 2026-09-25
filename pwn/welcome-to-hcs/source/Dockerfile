FROM debian:trixie

RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m hcs
WORKDIR /home/hcs

COPY chall /home/hcs/chall
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /home/hcs/chall && \
    chmod +x /entrypoint.sh && \
    chown root:root /home/hcs/chall && \
    chmod 755 /home/hcs/chall && \
    chown hcs:hcs /home/hcs

USER hcs
EXPOSE 4413

ENTRYPOINT ["/entrypoint.sh"]