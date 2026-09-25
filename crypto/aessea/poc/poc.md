# Penyelesaian

AES-ECB mengenkripsi tiap blok 16 byte secara terpisah. Karena itu, blok dari dua ticket dapat digabung untuk membuat ticket baru.

1. Minta ticket dengan nama `AAAAA`. Blok pertamanya berisi `name=AAAAA;role=`.
2. Minta ticket dengan nama berupa sebelas byte `A`, lalu `admin`, lalu sebelas byte `0x0b`. Blok keduanya berisi `admin` beserta padding PKCS#7.
3. Gabungkan blok pertama dari ticket pertama dengan blok kedua dari ticket kedua, lalu redeem hasilnya.
