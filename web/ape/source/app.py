import os
import subprocess
from pathlib import Path

from flask import Flask, render_template, abort, Response

app = Flask(__name__)

FLAG = os.environ.get("FLAG")

REPO_DIR = Path("/app/repo")
GIT_DIR = REPO_DIR / ".git"


def init_repo():
    if GIT_DIR.exists():
        return

    REPO_DIR.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["HOME"] = "/tmp"
    env["GIT_AUTHOR_NAME"] = "apesihape-dev"
    env["GIT_AUTHOR_EMAIL"] = "dev@apesihape.local"
    env["GIT_COMMITTER_NAME"] = "apesihape-dev"
    env["GIT_COMMITTER_EMAIL"] = "dev@apesihape.local"

    def run(*args):
        subprocess.run(
            ["git", "-C", str(REPO_DIR), *args],
            env=env,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    run("init", "-q", "-b", "main")
    run("config", "--local", "user.email", "dev@apesihape.local")
    run("config", "--local", "user.name", "apesihape-dev")

    notes_dir = REPO_DIR / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    (notes_dir / "internal.txt").write_text(FLAG + "\n")
    (REPO_DIR / "README_INTERNAL.md").write_text(
        "Internal staging notes.\nDO NOT ship this file with the site.\n"
    )
    run("add", ".")
    run("commit", "-q", "-m", "wip: internal staging notes")

    (notes_dir / "internal.txt").unlink()
    (REPO_DIR / "README_INTERNAL.md").write_text(
        "Internal staging notes.\n(cleaned up before going live)\n"
    )
    run("add", "-A")
    run("commit", "-q", "-m", "clean up before going live")


APP_NAME = "APE"


@app.route("/")
def index():
    return render_template("index.html", app_name=APP_NAME)


@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nDisallow: /.git/\n", mimetype="text/plain")


@app.route("/.git/<path:filepath>")
def serve_git(filepath):
    target = (GIT_DIR / filepath).resolve()
    try:
        target.relative_to(GIT_DIR.resolve())
    except ValueError:
        abort(403)

    if not target.is_file():
        abort(404)

    return Response(target.read_bytes(), mimetype="application/octet-stream")

init_repo()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5555)), threaded=True)
