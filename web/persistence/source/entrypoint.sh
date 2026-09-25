#!/bin/bash
set -e

if [ -z "${FLAG:-}" ]; then
    FLAG="HCS{th0s3_wh0_p3rs1st_4nd_4d4pt_w1n_$(cat /proc/sys/kernel/random/uuid)}"
fi

echo "$FLAG" > /flag.txt
chmod 644 /flag.txt
unset FLAG

exec apache2-foreground
