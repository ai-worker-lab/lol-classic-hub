#!/usr/bin/env python3
"""생성된 사이트의 MVP 계약을 빠르게 검증한다."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE = "/lol-classic-hub"
REQUIRED_PATHS = ["/", "/runes/", "/masteries/", "/season3-items/", "/champions/", "/builder/"]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self.links: list[str] = []
        self.images: list[str] = []
        self.scripts: list[tuple[str, str]] = []
        self.current_script_type = ""
        self.current_script = ""
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            key = values.get("name") or values.get("property")
            if key and values.get("content"):
                self.meta[key] = values["content"] or ""
        elif tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href") or ""
        elif tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        elif tag == "img" and values.get("src"):
            self.images.append(values["src"] or "")
        elif tag == "script":
            self.current_script_type = values.get("type") or ""
            self.current_script = ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        elif tag == "script":
            self.scripts.append((self.current_script_type, self.current_script))
            self.current_script_type = ""
            self.current_script = ""

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        if self.current_script_type:
            self.current_script += data
        self.text.append(data)


def file_for(path: str) -> Path:
    return SITE / "index.html" if path == "/" else SITE / path.lstrip("/") / "index.html"


def main() -> int:
    errors: list[str] = []
    for required in [SITE / "robots.txt", SITE / "sitemap.xml", SITE / "404.html", SITE / "assets/site.css", SITE / "assets/builder.js", SITE / "data-manifest.json"]:
        if not required.is_file():
            errors.append(f"필수 파일 없음: {required.relative_to(ROOT)}")

    expected_canonicals: set[str] = set()
    for path in REQUIRED_PATHS:
        page = file_for(path)
        if not page.is_file():
            errors.append(f"페이지 없음: {path}")
            continue
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        expected = f"https://ai-worker-lab.github.io{BASE}{path}"
        expected_canonicals.add(expected)
        if not parser.title.strip(): errors.append(f"title 없음: {path}")
        if not parser.meta.get("description"): errors.append(f"description 없음: {path}")
        if parser.meta.get("robots") != "index,follow,max-image-preview:large": errors.append(f"robots meta 오류: {path}")
        if parser.canonical != expected: errors.append(f"canonical 오류: {path} -> {parser.canonical}")
        for key in ["og:title", "og:description", "og:url"]:
            if not parser.meta.get(key): errors.append(f"{key} 없음: {path}")
        json_ld = [body for script_type, body in parser.scripts if script_type == "application/ld+json"]
        if not json_ld: errors.append(f"JSON-LD 없음: {path}")
        else:
            try: json.loads(json_ld[0])
            except json.JSONDecodeError as exc: errors.append(f"JSON-LD 오류: {path}: {exc}")
        text = " ".join(parser.text)
        if path in {"/runes/", "/masteries/", "/season3-items/", "/champions/"}:
            for marker in ["검토 중인 출처", "확인일", "확인 중", "3.15.5"]:
                if marker not in text: errors.append(f"출처 표식 '{marker}' 없음: {path}")
            if parser.images:
                errors.append(f"정책 검토 전 금지된 게임 에셋 노출: {path}")
        for link in parser.links:
            parsed = urlparse(link)
            if parsed.scheme or parsed.netloc or not parsed.path.startswith(BASE):
                continue
            relative = parsed.path.removeprefix(BASE) or "/"
            target = file_for(relative) if relative.endswith("/") else SITE / relative.lstrip("/")
            if not target.exists(): errors.append(f"깨진 내부 링크: {path} -> {link}")

    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8") if (SITE / "sitemap.xml").exists() else ""
    for url in expected_canonicals:
        if f"<loc>{url}</loc>" not in sitemap: errors.append(f"사이트맵 URL 없음: {url}")
    robots = (SITE / "robots.txt").read_text(encoding="utf-8") if (SITE / "robots.txt").exists() else ""
    if "Allow: /" not in robots or f"Sitemap: https://ai-worker-lab.github.io{BASE}/sitemap.xml" not in robots:
        errors.append("robots.txt 규칙 오류")
    builder = (SITE / "assets/builder.js").read_text(encoding="utf-8") if (SITE / "assets/builder.js").exists() else ""
    for token in ["localStorage.getItem", "localStorage.setItem", "remove"]:
        if token not in builder: errors.append(f"빌더 동작 토큰 없음: {token}")

    if re.search(r"(?:api[_-]?key|secret|password)\s*[:=]", "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in SITE.rglob("*") if path.is_file()), re.I):
        errors.append("배포 산출물에서 비밀정보 형태 문자열 감지")

    if errors:
        print("검증 실패")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    manifest = json.loads((SITE / "data-manifest.json").read_text(encoding="utf-8"))
    print(f"검증 성공: 페이지 {len(REQUIRED_PATHS)}개, 오류 0건")
    print("데이터 항목:", ", ".join(f"{key}={value}" for key, value in manifest["counts"].items()))
    print("필수 SEO: canonical/description/Open Graph/JSON-LD/robots/sitemap 확인")
    print("정책 게이트: 게임 데이터·이미지 에셋 미노출 확인")
    print("클라이언트 도구: localStorage 저장·삭제 코드 확인")
    return 0


if __name__ == "__main__":
    sys.exit(main())
