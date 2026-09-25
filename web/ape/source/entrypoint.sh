#!/bin/sh
set -e

if [ -z "${FLAG:-}" ]; then
    FLAG="HCS{gh4r0wwwwwwwwwwwwwwwwwwwww_k1ng_g1thub_gu3_4ku1n_$(head -c 16 /dev/urandom | md5sum | head -c 10)}"
fi

export FLAG
exec python app.py
