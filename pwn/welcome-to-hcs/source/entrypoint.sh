#!/bin/sh
set -e

RAND_NAME=$(head -c 16 /dev/urandom | md5sum | head -c 8)
RAND_SUFFIX=$(head -c 32 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 12)

FLAG_PATH="/home/hcs/flag-${RAND_NAME}.txt"

echo "HCS{goddamnnn_you_made_it_pals_see_you_in_HCS_^^_${RAND_SUFFIX}}" > "$FLAG_PATH"
chmod 400 "$FLAG_PATH"

exec socat TCP-LISTEN:4413,reuseaddr,fork EXEC:/home/hcs/chall,stderr