#!/bin/sh
set -e

RAND_NAME=$(head -c 16 /dev/urandom | md5sum | head -c 8)
RAND_SUFFIX=$(head -c 32 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 12)

FLAG_PATH="/home/ly/flag-${RAND_NAME}.txt"

echo "HCS{ret2reg_w1th_40_bytes_goes_brrrrrrrrrrrrr_${RAND_SUFFIX}}" > "$FLAG_PATH"
chmod 400 "$FLAG_PATH"

exec socat TCP-LISTEN:4411,reuseaddr,fork EXEC:/home/ly/chall,stderr