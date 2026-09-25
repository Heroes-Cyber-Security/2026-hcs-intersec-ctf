FROM debian:trixie

RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ly
WORKDIR /home/ly

COPY chall /home/ly/chall
COPY flag.txt /home/ly/flag.txt
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /home/ly/chall && \
    chmod +x /entrypoint.sh && \
    chown -R root:root /home/ly && \
    chmod 755 /home/ly && \
    chown root:root /home/ly/chall && \
    chmod 755 /home/ly/chall

USER ly
EXPOSE 4411

ENTRYPOINT ["/entrypoint.sh"]