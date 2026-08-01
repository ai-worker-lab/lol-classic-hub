#!/usr/bin/env python3
"""GitHub Pages 프로젝트 경로를 그대로 재현하는 로컬 정적 서버."""

from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE = "/lol-classic-hub"


class ProjectPagesHandler(SimpleHTTPRequestHandler):
    def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
        if code != 404:
            super().send_error(code, message, explain)
            return
        body = (SITE / "404.html").read_bytes()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def translate_path(self, path: str) -> str:
        parsed = urlsplit(path)
        clean_path = parsed.path
        if clean_path == BASE:
            clean_path = "/"
        elif clean_path.startswith(BASE + "/"):
            clean_path = clean_path[len(BASE):]
        rewritten = urlunsplit(("", "", clean_path, parsed.query, parsed.fragment))
        return super().translate_path(rewritten)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), lambda *args, **kwargs: ProjectPagesHandler(*args, directory=str(SITE), **kwargs))
    print(f"로컬 서버: http://127.0.0.1:8000{BASE}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
