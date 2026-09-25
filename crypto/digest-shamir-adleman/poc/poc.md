## 1. Bruteforce hash collision di `myHash()`

10^12 possible digest = ~10^6 computations (according to birthday problem)

Example pair:
`HG:cRwz`
`(Y>&9e"`

## 2. Decrypt received signature with RSA

RSA biasa, decrypt aja kyk biasa. N ada di factordb, dapetin D buat decrypt

```py
euler_tot = (P_RSA-1) * (Q_RSA-1)
D = pow(e, -1, euler_tot)

def decrypt_rsa(m, n, D):
    return pow(m,D, n)
```

## 3. DSA nonce reuse

Hash di step 1 dipake buat nonce DSA. karna digest sama, maka nonce jadi sama. `r` buat 2 signature jadi sama. lgsg extract `X` nya (hash function buat `e1` dan `e2` pake `md5_int()` yg ada di sc):

```py
def recover_key(e1, s1, e2, s2, r, q):
    """
    e1, e2: message digests
    s1, s2: signature s-values from the two signatures (must share same r)
    r: the shared r value
    q: DSA subgroup order
    """
    # k = (e1 - e2) / (s1 - s2)  mod q
    s_diff = (s1 - s2) % q
    e_diff = (e1 - e2) % q
    k = (e_diff * pow(s_diff, -1, q)) % q

    # x = (s1*k - e1) / r  mod q
    x = ((s1 * k - e1) * pow(r, -1, q)) % q

    return k, x
```

## 4. Convert x to flag

tinggal convert

```py
print(x.to_bytes((x.bit_length() + 7 ) // 8, "big").decode("utf-8"))
```
