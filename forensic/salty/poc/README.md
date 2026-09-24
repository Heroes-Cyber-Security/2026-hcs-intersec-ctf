# Salty

Stop salty mas!

## Walkthrough

Just small linux image, `DOS/MBR boot sector`, so let's use `losetup` to treat the image like a real block disk, then mount.

```bash
LOOP=$(sudo losetup --find --partscan --read-only --show salty.img)
echo "$LOOP"

sudo mkdir -p /mnt/salty
sudo mount -o ro,noload "${LOOP}p1" /mnt/salty
```

Find any file that have `*flag*`, got some interesting file:

```bash
/mnt/salty/root/flag.enc
/mnt/salty/root/flag.sha256
/mnt/salty/opt/recover_flag.py
```

On `recover_flag.py` we can get the flag by running the script with the encrypted flag, it hash, and the right salt.

So use the find command again and we got some files:

```bash
/mnt/salty/home/mirai/.local/share/.salt
/mnt/salty/home/mirai/.cache/.salt
/mnt/salty/home/ery/.config/.salt
/mnt/salty/home/ery/projects/.cache/.salt
/mnt/salty/home/elsche/.config/session/.salt
/mnt/salty/home/elsche/Documents/.backup/.salt
/mnt/salty/home/rutkido/.cache/archive/.salt
/mnt/salty/home/rutkido/projects/.state/.salt
/mnt/salty/home/grb/.local/state/.salt
/mnt/salty/home/grb/Documents/.old/.salt
```

```bash
find /mnt/salty/home -name '.salt' -type f 2>/dev/null |
while read -r salt; do
    echo "[*] Trying $salt"

    python3 solve/recover_flag.py \
        solve/flag.enc \
        "$salt" \
        solve/flag.sha256 2>/dev/null && break
done
```

All of them failed. Check deleted file:

```bash
fls -r -d -o 2048 salty.img
r/r * 505(realloc):	home/ery/projects/.metadata/.salt
```

Got another salt file, location is on inode 505, so use icat:
```bash
icat -o 2048 salty.img 505
```

Got the salt `halo_tolong_refund_piala_trims`, let's try to recover the flag.

```bash
python3 recover_flag.py flag.enc recovered.salt flag.sha256
```

Hore-hore, `HCS{bikin_soal_intersec_biar_my_kisah_bangga}`