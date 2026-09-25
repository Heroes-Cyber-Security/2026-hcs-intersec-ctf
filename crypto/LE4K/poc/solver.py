from pwn import *
from math import isqrt
from Crypto.Util.number import long_to_bytes, inverse

HOST = ''
PORT = 6767
ROUNDS = 5

def solve(n, e, c, qinv):
    for k in range(1, 2 * qinv):
        D = 1 + 4 * k * n * qinv
        s = isqrt(D)

        if s**2 != D:
            continue

        num = s - 1
        den = 2 * k

        if num % den != 0:
            continue

        p = num // den
        
        if p <= 1 or n % p != 0:
            continue

        q = n // p
        phi = (p - 1) * (q - 1)
        d = inverse(e, phi)
        m = pow(c, d, n)

        return long_to_bytes(m)

r = remote(HOST, PORT)

for rnd in range(ROUNDS):
    r.recvuntil(f"Round {r+1}\n".encode())
    n = int(rnd.recvline().decode().strip().split("=")[1])
    e = int(rnd.recvline().decode().strip().split("=")[1])
    c = int(rnd.recvline().decode().strip().split("=")[1])
    hmmm = int(rnd.recvline().decode().strip().split("=")[1])
    
    m = solve(n, e, c, hmmm)
    rnd.sendlineafter(b"(hex): ", m.hex().encode())

print(rnd.recvall().decode())
