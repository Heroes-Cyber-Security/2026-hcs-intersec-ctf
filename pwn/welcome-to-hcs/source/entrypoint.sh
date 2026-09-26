#!/bin/sh
set -eu

FLAG_PATH=/home/hcs/flag.txt

echo $CTF_FLAG > $FLAG_PATH

exec socat TCP-LISTEN:4413,reuseaddr,fork EXEC:/home/hcs/chall,stderr
