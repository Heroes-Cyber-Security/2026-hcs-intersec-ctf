# X-it 

A phone's camera roll got backed up before wipe. Nothing looks unusual at a glance. X it and you'll find the X key :)

## 1. Scan all files, spot the outlier

Pull the same metadata fields from all of them at once.
```
exiftool -a -G1 -s -UserComment -Make -Model -Software -ThumbnailImage DCIM_Camera/*.JPG
```
`IMG_2501.JPG` is the odd one out. Its `UserComment` is a hex blob and its `ThumbnailImage` is also the largest compared to the other images.
```
======== DCIM_Camera/IMG_2501.JPG
[ExifIFD]       UserComment                     : PAYLOAD(XOR-HEX): 0f31670275495d03727e48535733116c3646056e070c192f003b051a5828095a6e05030a22072c1f510a26263a4e
[IFD0]          Make                            : Apple
[IFD0]          Model                           : iPhone 13
[IFD0]          Software                        : 17.5.1
[IFD1]          ThumbnailImage                  : (Binary data 1695 bytes, use -b option to extract)
```

## 2. Extract its thumbnail

`exiftool` never shows the thumbnail's actual bytes, just a "(Binary data ...)" notice. Extract it to see what's really inside.
```
exiftool -b -ThumbnailImage DCIM_Camera/IMG_2501.JPG > thumb.jpg
```
Output:
```
thumb.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=2, software=Adobe Photoshop 25.0 (Macintosh)], baseline, precision 8, 160x120, components 3
```
`file thumb.jpg` shows it's its own JPEG with its own EXIF, `Software: Adobe Photoshop` doesn't match the outer file's `iPhone 13`. A thumbnail's EXIF should just be whatever the camera wrote, so a different tool's signature means someone edited it after. Treat it as its own file and check it the same way as step 1.

## 3. Pull the raw bytes of the thumbnail's UserComment

Its `UserComment` isn't readable text, so pipe the raw bytes (`-b`) into `xxd` instead of printing it directly.
```
exiftool -b -UserComment thumb.jpg | xxd
```
Output:
```
00000000: ecfb fdf1 e8fb ece7 c1f5 fbe7 a3d9 ecaa  ................
00000010: e7d8 aff2 fbb3 d3ae fcaf f2fb c1da ade8  ................
00000020: affd fbb3 dfeb faaf eab3 ddf6 aaaf f0ae  ................
00000030: f8dd ebed eaae fae7 c1cc adfd aee8 adec  ................
00000040: e7c1 d5ad e7c1 acae aca8 bf              ...........
```
Hex:
`ecfbfdf1e8fbece7c1f5fbe7a3d9ecaae7d8aff2fbb3d3aefcaff2fbc1daade8affdfbb3dfebfaafeab3ddf6aaaff0aef8ddebedeaaefae7c1ccadfdaee8adece7c1d5ade7c1acaeaca8bf`

Every byte is high-value (0xA3 -> 0xFD). That's what printable text looks like after being XOR'd with one fixed byte that has its high bit set. A sign this is hidden text, not random data.

## 4. Brute-force the 1-byte key

A single-byte key only has 256 possible values. Try them all and keep the one that decodes to readable text.

_optional: can be done in CyberChef_

Recipe: `From Hex` -> `XOR Brute Force` (paste the hex from step 3, crib = `key`)

[Here is the Recipe](https://cyberchef.io/#recipe=From_Hex('Auto')XOR_Brute_Force(1,100,0,'Standard',false,true,false,'key')&input=ZWNmYiBmZGYxIGU4ZmIgZWNlNyBjMWY1IGZiZTcgYTNkOSBlY2FhIGU3ZDggYWZmMiBmYmIzIGQzYWUgZmNhZiBmMmZiIGMxZGEgYWRlOCBhZmZkIGZiYjMgZGZlYiBmYWFmIGVhYjMgZGRmNiBhYWFmIGYwYWUgZjhkZCBlYmVkIGVhYWUgZmFlNyBjMWNjIGFkZmQgYWVlOCBhZGVjIGU3YzEgZDVhZCBlN2MxIGFjYWUgYWNhOCBiZg)

Output:
`Key = 9e: recovery_key=Gr4yF1le-M0b1le_D3v1ce-Aud1t-Ch41n0fCust0dy_R3c0v3ry_K3y_2026!`

## 5. Decrypt the flag

Step 1's hex blob was ciphertext with no key yet. Step 4 just found the key. XOR them together to get the flag.

_optional: can be done in CyberChef_

Recipe: `From Hex` (paste the ciphertext from step 1) -> `XOR` (Key = `Gr4yF1le-M0b1le_D3v1ce-Aud1t-Ch41n0fCust0dy_R3c0v3ry_K3y_2026!`, type UTF8)

[Here is the Recipe](https://cyberchef.io/#recipe=From_Hex('Auto')XOR(%7B'option':'UTF8','string':'Gr4yF1le-M0b1le_D3v1ce-Aud1t-Ch41n0fCust0dy_R3c0v3ry_K3y_2026!'%7D,'Standard',false)&input=MGYzMTY3MDI3NTQ5NWQwMzcyN2U0ODUzNTczMzExNmMzNjQ2MDU2ZTA3MGMxOTJmMDAzYjA1MWE1ODI4MDk1YTZlMDUwMzBhMjIwNzJjMWY1MTBhMjYyNjNhNGU)

Flag: `HCS{3x1f_3x1f_t3rus_di4nu_4nukan_k3lar_kan_yh}`
