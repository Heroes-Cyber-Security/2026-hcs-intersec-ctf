FROM debian:trixie

RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m hcs
WORKDIR /home/hcs

COPY chall /home/hcs/chall
COPY flag.txt /home/hcs/flag.txt
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /home/hcs/chall && \
    chmod +x /entrypoint.sh && \
    chown -R root:root /home/hcs && \
    chmod 755 /home/hcs && \
    chown root:root /home/hcs/chall && \
    chmod 755 /home/hcs/chall && \
    chown root:root /home/hcs/flag.txt && \
    chmod 444 /home/hcs/flag.txt

USER hcs
EXPOSE 4413

ENTRYPOINT ["/entrypoint.sh"]
