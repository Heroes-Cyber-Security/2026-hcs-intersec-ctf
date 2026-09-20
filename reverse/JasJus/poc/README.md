# PoC - JasJus

Reverse `check()` dari `challenge.js` doang, tinggal dibalik.

## Logic Encode

```
char -> XOR key[13,37,42] -> + i*3 + 7 -> reverse array
```

## PoC Standalone

```js
const _k = [13, 37, 42];
const _d = [
  33, 61, 50, 3, 56, 254, 35, 200, 245, 26, 8, 226, 184, 29, 227, 182, 251, 211,
  237, 209, 237, 5, 2, 193, 157, 143, 181, 238, 228, 181, 126, 130, 232, 220,
  209, 173, 121, 108, 161, 192, 204, 176, 182, 96, 170, 155, 131, 169, 175, 160,
  120, 67, 146, 142, 157, 118, 91, 134, 129, 122, 101, 20, 134, 134, 112, 76,
];

let rev = [..._d].reverse();
let flag = '';
for (let i = 0; i < rev.length; i++) {
  let c = (rev[i] - i * 3 - 7) & 0xff;
  c = c ^ _k[i % _k.length];
  flag += String.fromCharCode(c);
}
console.log(flag);
```

Stepnya cuma:

1. `reverse()` biar urutan normal lagi
2. `- i*3 - 7` buat balikin `+ i*3 + 7`
3. `XOR` lagi pake key yg sama
