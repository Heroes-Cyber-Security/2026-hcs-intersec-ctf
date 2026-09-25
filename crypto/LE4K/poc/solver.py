from pwn import *
from math import isqrt
from Crypto.Util.number import long_to_bytes, inverse

HOST = 'le4k-6e4eaa974291.challenge.hcs-team.com'
PORT = 1337
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

r = remote(HOST, PORT, ssl=True)

for rnd in range(ROUNDS):
    r.recvuntil(f"Round {rnd+1}\n".encode())
    n = int(r.recvline().decode().strip().split("=")[1])
    e = int(r.recvline().decode().strip().split("=")[1])
    c = int(r.recvline().decode().strip().split("=")[1])
    hmmm = int(r.recvline().decode().strip().split("=")[1])
    
    m = solve(n, e, c, hmmm)
    r.sendlineafter(b"(hex): ", m.hex().encode())

print(r.recvall().decode())
