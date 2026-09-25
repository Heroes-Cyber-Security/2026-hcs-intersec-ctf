#!/bin/bash
set -e

if [ -z "${FLAG:-}" ]; then
    FLAG="HCS{th0s3_wh0_p3rs1st_4nd_4d4pt_w1n_4nd_sh4ll_ev0lve_thr0ugh_th3_shad0ws_$(cat /proc/sys/kernel/random/uuid)}"
fi

FLAG_PATH="/flag_$(cat /proc/sys/kernel/random/uuid)"
echo "$FLAG" > "$FLAG_PATH"
chmod 644 "$FLAG_PATH"
unset FLAG FLAG_PATH

exec apache2-foreground
