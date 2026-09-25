#!/bin/sh
set -e

exec socat TCP-LISTEN:4412,reuseaddr,fork EXEC:/home/hcs/chall,stderr
