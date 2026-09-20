FROM debian:trixie@sha256:9cc080028c43b27d2074d63a5f9caf7166d731494965616c1a6d2827a004585c
# digest pinned: the runtime libc stays identical to the libc in release/chall.zip

RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m gosip
WORKDIR /home/gosip

COPY chall /home/gosip/chall
COPY flag.txt /home/gosip/flag.txt

RUN chmod +x /home/gosip/chall && \
    chown -R root:root /home/gosip && \
    chmod 755 /home/gosip && \
    chown gosip:gosip /home/gosip/flag.txt && \
    chmod 400 /home/gosip/flag.txt

USER gosip
EXPOSE 4412

CMD ["socat", "TCP-LISTEN:4412,reuseaddr,fork", "EXEC:/home/gosip/chall,stderr"]
