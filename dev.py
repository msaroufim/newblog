#!/usr/bin/env python3
from __future__ import annotations

import functools
import http.server
import os
import threading
import time
from pathlib import Path

import build


ROOT = Path(__file__).parent
WATCH_DIRS = [
    ROOT / "_posts",
    ROOT / "_drafts",
    ROOT / "_data",
    ROOT / "assets",
]
WATCH_FILES = [
    ROOT / "build.py",
    ROOT / "dev.py",
    ROOT / "index.md",
    ROOT / "blog.md",
    ROOT / "talks.md",
    ROOT / "bookshelf.md",
    ROOT / "404.html",
    ROOT / "README.md",
    ROOT / "pyproject.toml",
]
POLL_INTERVAL_SECONDS = 1.0


def snapshot() -> dict[Path, float]:
    mtimes: dict[Path, float] = {}
    for path in WATCH_FILES:
        if path.exists():
            mtimes[path] = path.stat().st_mtime
    for directory in WATCH_DIRS:
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.is_file():
                mtimes[path] = path.stat().st_mtime
    return mtimes


def build_site() -> None:
    build.main()
    print("rebuilt _site")


def watch() -> None:
    last_seen = snapshot()
    while True:
        time.sleep(POLL_INTERVAL_SECONDS)
        current = snapshot()
        if current != last_seen:
            build_site()
            last_seen = current


def main() -> None:
    port = int(os.environ.get("PORT", "8000"))
    build_site()

    watcher = threading.Thread(target=watch, daemon=True)
    watcher.start()

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT / "_site"))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print(f"serving http://127.0.0.1:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
