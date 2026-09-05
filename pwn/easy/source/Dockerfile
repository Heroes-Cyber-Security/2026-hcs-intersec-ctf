from DEBIAN:trixie

RUN apt-get update && apt-get install -y \
    socat\
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ly
WORKDIR /home/ly

COPY chall /home/ly/chall
COPY flag.txt /home/ly/flag.txt

RUN chmod +x /home/ly/chall && \
    chown -R root:root /home/ly && \
    chmod 755 /home/ly && \
    chown 755 /home/ly/chall && \
    chown ly:ly /home/ly/flag.txt && \
    chmod 400 /home/ly/flag.txt

USER ly
EXPOSE 4411

CMD ["socat", "TCP-LISTEN:4411,reuseaddr,fork", "EXEC:/home/ly/chall,stderr"]