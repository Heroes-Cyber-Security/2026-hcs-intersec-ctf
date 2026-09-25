#!/bin/sh
set -e

RAND_NAME=$(head -c 16 /dev/urandom | md5sum | head -c 8)
RAND_SUFFIX=$(head -c 32 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 12)

FLAG_PATH="/home/ly/flag-${RAND_NAME}.txt"

echo "HCS{g0s1p_g0s1p_p0ps_4_sh3ll_l34ky_l1br4ry_${RAND_SUFFIX}}" > "$FLAG_PATH"
chmod 400 "$FLAG_PATH"

exec socat TCP-LISTEN:4412,reuseaddr,fork EXEC:/home/gosip/chall,stderr