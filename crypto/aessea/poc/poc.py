import sys

from pwn import *


def make_ticket(io, name):
    io.sendlineafter(b">> ", b"1")
    io.sendlineafter(b"Name (hex): ", name.hex().encode())
    io.recvuntil(b"Ticket: ")
    return bytes.fromhex(io.recvline().strip().decode())


host = ""
port = 5001

io = remote(host, port)
try:
    base = make_ticket(io, b"A" * 5)
    admin = make_ticket(io, b"A" * 11 + b"admin" + bytes([11]) * 11)
    forged = base[:16] + admin[16:32]

    io.sendlineafter(b">> ", b"2")
    io.sendlineafter(b"Ticket (hex): ", forged.hex().encode())
    result = io.recvline().decode().strip()
    assert result.startswith("HCS{"), result
    print(result)
    io.sendlineafter(b">> ", b"3")
finally:
    io.close()
