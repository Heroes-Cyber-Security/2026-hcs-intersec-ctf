FROM debian:trixie

RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ly
WORKDIR /home/ly

COPY chall /home/ly/chall
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /home/ly/chall && \
    chmod +x /entrypoint.sh && \
    chown root:root /home/ly/chall && \
    chmod 755 /home/ly/chall && \
    chown ly:ly /home/ly

USER ly
EXPOSE 4411

ENTRYPOINT ["/entrypoint.sh"]