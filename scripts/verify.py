#!/usr/bin/env python3
"""생성된 공개 사이트의 데이터·에셋·고지·SEO 계약을 검증한다."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
BASE = "/lol-classic-hub"
VERSION = "3.13.24"
LOCALE = "ko_KR"
POLICY_REVIEWED_AT = "2026-08-02"
REQUIRED_PATHS = ["/", "/runes/", "/masteries/", "/season3-items/", "/champions/", "/builder/"]
EXPECTED_ITEM_DETAIL_PAGES = 205
EXPECTED_FROM_ITEMS = 158
EXPECTED_INTO_ITEMS = 65
EXPECTED_FROM_REFS = 279
EXPECTED_INTO_REFS = 267
DATA_PATHS = {
    "/runes/": ("runes", 296),
    "/masteries/": ("masteries", 56),
    "/season3-items/": ("items", 205),
    "/champions/": ("champions", 116),
}
DATA_FILES = {"champions":"champion.json","items":"item.json","masteries":"mastery.json","runes":"rune.json"}
OFFICIAL_DATA_SHA256 = {
    "champions": "d073d5a023cb700118c3d63652b15d11fb8e213896897828cc024daef0cea925",
    "items": "cecc6ed683f80f076f0888053648f9604017155a9f9cc3ad2d9b47c3f8254bbe",
    "masteries": "2fd552d4fbf4cb25b5b4e1ba6e7bd7e7a3ba1dc1a63cbfe3fef34e57385a53ae",
    "runes": "de3d476f130bacd46e122acbc9a5a95fa2a1af94c8fce1d422297b1de795857f",
}
EXPECTED_IMAGE_REFERENCES = 673
EXPECTED_UNIQUE_IMAGES = 447
LEGAL_MARKERS = [
    "isn't endorsed by Riot Games",
    "was created under Riot Games' \"Legal Jibber Jabber\" policy",
    "광고·결제·후원·유료 기능 없음",
]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self.links: list[str] = []
        self.images: list[str] = []
        self.image_alts: list[str] = []
        self.scripts: list[tuple[str, str]] = []
        self.current_script_type = ""
        self.current_script = ""
        self.text: list[str] = []
        self.item_node_labels: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if "item-node" in (values.get("class") or "").split():
            self.item_node_labels.append(values.get("aria-label") or "")
        if tag == "title": self.in_title = True
        elif tag == "meta":
            key = values.get("name") or values.get("property")
            if key and values.get("content"): self.meta[key] = values["content"] or ""
        elif tag == "link" and values.get("rel") == "canonical": self.canonical = values.get("href") or ""
        elif tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        elif tag == "img" and values.get("src"):
            self.images.append(values["src"] or "")
            self.image_alts.append(values.get("alt") or "")
        elif tag == "script":
            self.current_script_type = values.get("type") or ""
            self.current_script = ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "title": self.in_title = False
        elif tag == "script":
            self.scripts.append((self.current_script_type, self.current_script))
            self.current_script_type = ""
            self.current_script = ""

    def handle_data(self, data: str) -> None:
        if self.in_title: self.title += data
        if self.current_script_type: self.current_script += data
        self.text.append(data)


def file_for(path: str) -> Path:
    return SITE / "index.html" if path == "/" else SITE / path.lstrip("/") / "index.html"


def public_file(url_path: str) -> Path:
    relative = url_path.removeprefix(BASE).lstrip("/")
    return SITE / relative


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relation_has_cycle(items: dict[str, dict[str, object]], relation_key: str) -> bool:
    def visit(item_id: str, path: frozenset[str]) -> bool:
        if item_id in path:
            return True
        refs = items.get(item_id, {}).get(relation_key)
        return isinstance(refs, list) and any(visit(str(ref), path | {item_id}) for ref in refs if str(ref) in items)
    return any(visit(item_id, frozenset()) for item_id in items)


def expected_purchase(entry: dict[str, object]) -> str:
    gold = entry.get("gold")
    value = entry.get("purchasable")
    if value is None and isinstance(gold, dict):
        value = gold.get("purchasable")
    return "가능" if value is True else "불가" if value is False else "데이터 없음"


def expected_badges(entry: dict[str, object]) -> list[str]:
    badges = ["구매 불가"] if expected_purchase(entry) == "불가" else []
    maps = entry.get("maps")
    if isinstance(maps, dict):
        excluded = [str(map_id) for map_id, available in maps.items() if available is False]
        included = [str(map_id) for map_id, available in maps.items() if available is True]
        badges.extend(f"맵 {map_id} 제외" for map_id in excluded)
        if included and not excluded:
            badges.append("맵 " + ", ".join(included) + " 전용")
    return badges


def expected_node_label(entry: dict[str, object], item_id: str, quantity: int = 1) -> str:
    gold_value = entry.get("gold")
    gold: dict[str, object] = gold_value if isinstance(gold_value, dict) else {}
    quantity_label = f" {quantity}개 필요" if quantity > 1 else ""
    badges = expected_badges(entry)
    badge_label = " 배지: " + ", ".join(badges) if badges else ""
    return (
        f"{entry.get('name', '이름 없음')}{quantity_label} 아이템 ID {item_id} "
        f"총 가격 {gold.get('total', '데이터 없음')} · 조합 비용 {gold.get('base', '데이터 없음')} "
        f"구매 {expected_purchase(entry)}{badge_label}"
    )


def expected_relation_labels(
    refs: list[object],
    items: dict[str, dict[str, object]],
    relation_key: str,
    *,
    depth: int = 0,
    max_depth: int = 8,
    visited: frozenset[str] = frozenset(),
) -> list[str]:
    if depth >= max_depth:
        return []
    labels: list[str] = []
    for item_id, quantity in Counter(str(ref) for ref in refs).items():
        if item_id in visited:
            continue
        entry = items.get(item_id)
        if entry is None:
            continue
        labels.append(expected_node_label(entry, item_id, quantity))
        child_value = entry.get(relation_key)
        if item_id not in visited and isinstance(child_value, list) and child_value:
            labels.extend(expected_relation_labels(
                child_value,
                items,
                relation_key,
                depth=depth + 1,
                max_depth=max_depth,
                visited=visited | {item_id},
            ))
    return labels


def main() -> int:
    errors: list[str] = []
    required_files = [SITE/"robots.txt",SITE/"sitemap.xml",SITE/"404.html",SITE/"assets/site.css",SITE/"assets/builder.js",SITE/"assets/item-search.js",SITE/"data-manifest.json"]
    for required in required_files:
        if not required.is_file(): errors.append(f"필수 파일 없음: {required.relative_to(ROOT)}")

    manifest = json.loads((SITE/"data-manifest.json").read_text(encoding="utf-8")) if (SITE/"data-manifest.json").is_file() else {}
    if manifest.get("sourceVersion") != VERSION: errors.append("매니페스트 버전 오류")
    if manifest.get("locale") != LOCALE: errors.append("매니페스트 로케일 오류")
    if manifest.get("publicDistribution") is not True: errors.append("공개 게이트가 true가 아님")
    expected_counts = {key: count for _, (key, count) in DATA_PATHS.items()}
    if manifest.get("counts") != expected_counts: errors.append(f"매니페스트 개수 오류: {manifest.get('counts')}")

    expected_canonicals: set[str] = set()
    page_image_paths: list[str] = []
    total_images = 0
    for path in REQUIRED_PATHS:
        page = file_for(path)
        if not page.is_file():
            errors.append(f"페이지 없음: {path}")
            continue
        parser = PageParser(); parser.feed(page.read_text(encoding="utf-8"))
        expected = f"https://ai-worker-lab.github.io{BASE}{path}"
        expected_canonicals.add(expected)
        if not parser.title.strip(): errors.append(f"title 없음: {path}")
        if not parser.meta.get("description"): errors.append(f"description 없음: {path}")
        if parser.meta.get("robots") != "index,follow,max-image-preview:large": errors.append(f"robots meta 오류: {path}")
        if parser.canonical != expected: errors.append(f"canonical 오류: {path} -> {parser.canonical}")
        for key in ["og:title","og:description","og:url"]:
            if not parser.meta.get(key): errors.append(f"{key} 없음: {path}")
        json_ld = [body for script_type, body in parser.scripts if script_type == "application/ld+json"]
        if not json_ld: errors.append(f"JSON-LD 없음: {path}")
        else:
            try: json.loads(json_ld[0])
            except json.JSONDecodeError as exc: errors.append(f"JSON-LD 오류: {path}: {exc}")
        text = " ".join(parser.text)
        for marker in LEGAL_MARKERS:
            if marker not in text: errors.append(f"필수 고지 '{marker}' 없음: {path}")
        if path in DATA_PATHS:
            key, count = DATA_PATHS[path]
            for marker in [VERSION, LOCALE, "공식 출처", "확인일", "현행"]:
                if marker not in text: errors.append(f"출처 표식 '{marker}' 없음: {path}")
            if len(parser.images) != count: errors.append(f"이미지 개수 오류: {path} {len(parser.images)} != {count}")
            total_images += len(parser.images)
            if any(not alt.strip() for alt in parser.image_alts): errors.append(f"빈 이미지 alt: {path}")
            for image in parser.images:
                expected_prefix = f"{BASE}/assets/riot-data-dragon/{VERSION}/img/"
                if not image.startswith(expected_prefix): errors.append(f"비공식 이미지 경로: {path} -> {image}")
                else:
                    page_image_paths.append(urlparse(image).path.removeprefix(expected_prefix))
                    if not public_file(urlparse(image).path).is_file(): errors.append(f"이미지 파일 없음: {image}")
        elif parser.images:
            errors.append(f"예상하지 않은 이미지: {path}")
        for link in parser.links:
            parsed = urlparse(link)
            if parsed.scheme or parsed.netloc or not parsed.path.startswith(BASE): continue
            relative = parsed.path.removeprefix(BASE) or "/"
            target = file_for(relative) if relative.endswith("/") else SITE / relative.lstrip("/")
            if not target.exists(): errors.append(f"깨진 내부 링크: {path} -> {link}")

    if total_images != EXPECTED_IMAGE_REFERENCES: errors.append(f"전체 데이터 이미지 참조 오류: {total_images} != {EXPECTED_IMAGE_REFERENCES}")

    asset_manifest_path = ROOT/"assets/manifest.json"
    asset_manifest: dict[str, object] = {}
    if not asset_manifest_path.is_file():
        errors.append("에셋 매니페스트 없음: assets/manifest.json")
    else:
        try:
            loaded_asset_manifest = json.loads(asset_manifest_path.read_text(encoding="utf-8"))
            if isinstance(loaded_asset_manifest, dict):
                asset_manifest = loaded_asset_manifest
            else:
                errors.append("에셋 매니페스트 스키마 오류: 최상위 값이 객체가 아님")
        except json.JSONDecodeError as exc:
            errors.append(f"에셋 매니페스트 JSON 오류: {exc}")

    policy = asset_manifest.get("policy")
    if not isinstance(policy, dict) or policy.get("public_distribution") is not True:
        errors.append("에셋 공개 정책 게이트가 true가 아님")
    elif policy.get("status") != "공개 가능 (조건부)":
        errors.append(f"에셋 공개 정책 상태 오류: {policy.get('status')}")
    elif policy.get("reviewed_at") != POLICY_REVIEWED_AT:
        errors.append(f"에셋 공개 정책 확인일 오류: {policy.get('reviewed_at')}")
    datasets_rows = asset_manifest.get("datasets")
    available_asset_rows = asset_manifest.get("assets")
    excluded_rows = asset_manifest.get("not_provided_by_archive")
    if not isinstance(datasets_rows, list):
        errors.append("에셋 매니페스트 스키마 오류: datasets 배열 없음")
        datasets_rows = []
    if not isinstance(available_asset_rows, list):
        errors.append("에셋 매니페스트 스키마 오류: assets 배열 없음")
        available_asset_rows = []
    if not isinstance(excluded_rows, list):
        errors.append("에셋 매니페스트 스키마 오류: not_provided_by_archive 배열 없음")
        excluded_rows = []
    if len(datasets_rows) != 4:
        errors.append(f"에셋 매니페스트 데이터셋 수 오류: {len(datasets_rows)} != 4")
    if len(available_asset_rows) != EXPECTED_IMAGE_REFERENCES:
        errors.append(
            f"에셋 매니페스트 공개 에셋 수 오류: {len(available_asset_rows)} != {EXPECTED_IMAGE_REFERENCES}"
        )
    if len(excluded_rows) != 1:
        errors.append(f"에셋 매니페스트 공개 제외 수 오류: {len(excluded_rows)} != 1")
    distribution_rows = [*datasets_rows, *available_asset_rows]
    if any(
        not isinstance(row, dict)
        or row.get("public_distribution") is not True
        or row.get("policy_status") != "공개 가능 (조건부)"
        for row in distribution_rows
    ):
        errors.append("공개 데이터·에셋의 정책 상태가 조건부 공개/true와 일치하지 않음")
    if any(
        not isinstance(row, dict)
        or row.get("public_distribution") is not False
        or row.get("policy_status") != "공식 아카이브 미제공으로 공개 대상 제외"
        for row in excluded_rows
    ):
        errors.append("공식 아카이브 미제공 항목의 정책 상태가 공개 제외/false와 일치하지 않음")
    policy_summary = asset_manifest.get("summary", {})
    expected_policy_summary = {
        "policy_pending_count": 0,
        "public_distribution_count": 677,
        "excluded_from_distribution_count": 1,
    }
    if not isinstance(policy_summary, dict):
        errors.append("에셋 매니페스트 스키마 오류: summary 객체 없음")
    else:
        for key, expected in expected_policy_summary.items():
            if policy_summary.get(key) != expected:
                errors.append(f"에셋 매니페스트 summary.{key} 오류: {policy_summary.get(key)} != {expected}")

    asset_refs = available_asset_rows
    if not isinstance(asset_refs, list):
        errors.append("에셋 매니페스트 스키마 오류: assets 배열 없음")
        asset_refs = []
    if len(asset_refs) != EXPECTED_IMAGE_REFERENCES:
        errors.append(f"에셋 매니페스트 논리 참조 수 오류: {len(asset_refs)} != {EXPECTED_IMAGE_REFERENCES}")

    manifest_images: dict[str, str] = {}
    manifest_reference_paths: list[str] = []
    manifest_prefix = Path("vendor/riot-data-dragon")/VERSION/"img"
    for index, ref in enumerate(asset_refs):
        if not isinstance(ref, dict):
            errors.append(f"에셋 매니페스트 스키마 오류: assets[{index}]가 객체가 아님")
            continue
        file_value, expected_sha = ref.get("file"), ref.get("sha256")
        if not isinstance(file_value, str) or not isinstance(expected_sha, str):
            errors.append(f"에셋 매니페스트 스키마 오류: assets[{index}]의 file/sha256이 문자열이 아님")
            continue
        if not re.fullmatch(r"[0-9a-f]{64}", expected_sha):
            errors.append(f"에셋 매니페스트 SHA-256 형식 오류: assets[{index}] -> {expected_sha}")
            continue
        try:
            relative = Path(file_value).relative_to(manifest_prefix)
        except ValueError:
            errors.append(f"에셋 매니페스트 이미지 경로 오류: assets[{index}] -> {file_value}")
            continue
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"에셋 매니페스트 안전하지 않은 경로: assets[{index}] -> {file_value}")
            continue
        relative_text = relative.as_posix()
        manifest_reference_paths.append(relative_text)
        previous_sha = manifest_images.setdefault(relative_text, expected_sha)
        if previous_sha != expected_sha:
            errors.append(f"에셋 매니페스트 중복 경로 SHA-256 충돌: {relative_text}")

    if len(manifest_images) != EXPECTED_UNIQUE_IMAGES:
        errors.append(f"에셋 매니페스트 고유 이미지 수 오류: {len(manifest_images)} != {EXPECTED_UNIQUE_IMAGES}")
    if Counter(page_image_paths) != Counter(manifest_reference_paths):
        errors.append("페이지 이미지 논리 참조가 assets/manifest.json과 일치하지 않음")

    image_roots = {
        "vendor 원본": ROOT/"assets/vendor/riot-data-dragon"/VERSION/"img",
        "배포 site 복사본": SITE/"assets/riot-data-dragon"/VERSION/"img",
    }
    expected_image_paths = set(manifest_images)
    unique_images: list[Path] = []
    for label, image_root in image_roots.items():
        actual_image_paths = {
            path.relative_to(image_root).as_posix()
            for path in image_root.rglob("*")
            if path.is_file()
        } if image_root.is_dir() else set()
        missing = expected_image_paths - actual_image_paths
        extra = actual_image_paths - expected_image_paths
        if missing:
            errors.append(f"{label} 이미지 누락 {len(missing)}개: {', '.join(sorted(missing)[:5])}")
        if extra:
            errors.append(f"{label} 추가 이미지 {len(extra)}개: {', '.join(sorted(extra)[:5])}")
        if len(actual_image_paths) != EXPECTED_UNIQUE_IMAGES:
            errors.append(f"{label} 고유 이미지 파일 수 오류: {len(actual_image_paths)} != {EXPECTED_UNIQUE_IMAGES}")
        for relative_text, expected_sha in manifest_images.items():
            image_path = image_root/relative_text
            if not image_path.is_file():
                continue
            actual_sha = sha256_file(image_path)
            if actual_sha != expected_sha:
                errors.append(f"{label} 이미지 SHA-256 불일치: {relative_text} (실제 {actual_sha}, 기대 {expected_sha})")
        if label == "배포 site 복사본":
            unique_images = [image_root/relative for relative in actual_image_paths]

    if manifest.get("uniqueImages") != EXPECTED_UNIQUE_IMAGES: errors.append("매니페스트 고유 이미지 수 오류")
    if any(re.search(r"riot.*logo|league.*logo", p.name, re.I) for p in unique_images): errors.append("Riot/League 로고 파일 감지")

    data_root = ROOT/"assets/upstream"/VERSION/"data"/LOCALE
    for key, filename in DATA_FILES.items():
        data_path = data_root/filename
        if not data_path.is_file():
            errors.append(f"공식 데이터 파일 없음: {data_path.relative_to(ROOT)}")
            continue
        digest = sha256_file(data_path)
        official_sha = OFFICIAL_DATA_SHA256[key]
        if digest != official_sha:
            errors.append(f"공식 데이터 SHA-256 불일치: {filename} (실제 {digest}, 기대 {official_sha})")
        manifest_sha = manifest.get("dataSha256",{}).get(key)
        if manifest_sha != official_sha:
            errors.append(f"배포 데이터 매니페스트 SHA-256 불일치: {key} (실제 {manifest_sha}, 기대 {official_sha})")

    item_payload = json.loads((data_root/"item.json").read_text(encoding="utf-8"))
    raw_items = item_payload["data"]
    items: dict[str, dict[str, object]] = {str(item_id): entry for item_id, entry in raw_items.items() if isinstance(entry, dict)}
    def refs_for(entry: dict[str, object], key: str) -> list[object]:
        value = entry.get(key)
        return value if isinstance(value, list) else []
    from_items = sum(bool(refs_for(entry, "from")) for entry in items.values())
    into_items = sum(bool(refs_for(entry, "into")) for entry in items.values())
    from_refs = sum(len(refs_for(entry, "from")) for entry in items.values())
    into_refs = sum(len(refs_for(entry, "into")) for entry in items.values())
    if (from_items, into_items, from_refs, into_refs) != (EXPECTED_FROM_ITEMS, EXPECTED_INTO_ITEMS, EXPECTED_FROM_REFS, EXPECTED_INTO_REFS):
        errors.append(f"아이템 관계 수치 오류: from 보유/into 보유/from 참조/into 참조 = {from_items}/{into_items}/{from_refs}/{into_refs}")
    missing_refs = sorted({str(ref) for entry in items.values() for key in ("from", "into") for ref in refs_for(entry, key) if str(ref) not in items})
    if missing_refs:
        errors.append(f"누락 아이템 참조 {len(missing_refs)}개: {', '.join(missing_refs[:5])}")
    for relation_key in ("from", "into"):
        if relation_has_cycle(items, relation_key):
            errors.append(f"아이템 {relation_key} 순환 관계 감지")

    detail_dirs = [path for path in (SITE/"season3-items").iterdir() if path.is_dir()]
    if len(detail_dirs) != EXPECTED_ITEM_DETAIL_PAGES:
        errors.append(f"아이템 상세 페이지 수 오류: {len(detail_dirs)} != {EXPECTED_ITEM_DETAIL_PAGES}")
    for item_id, entry in items.items():
        path = f"/season3-items/{item_id}/"
        page = file_for(path)
        if not page.is_file():
            errors.append(f"아이템 상세 페이지 없음: {item_id}")
            continue
        source = page.read_text(encoding="utf-8")
        parser = PageParser(); parser.feed(source)
        expected = f"https://ai-worker-lab.github.io{BASE}{path}"
        expected_canonicals.add(expected)
        if parser.canonical != expected:
            errors.append(f"아이템 canonical 오류: {item_id} -> {parser.canonical}")
        if parser.meta.get("robots") != "index,follow,max-image-preview:large":
            errors.append(f"아이템 robots meta 오류: {item_id}")
        item_name = str(entry.get("name", "이름 없음"))
        page_name = f"{item_name} 조합·업그레이드 트리"
        full_page_name = f"{page_name} | 클래식 노트"
        page_description = f"{item_name}의 시즌 3 하위 조합 재료, 가격, 상위 업그레이드 트리."
        if parser.title != full_page_name or parser.meta.get("description") != page_description:
            errors.append(f"아이템 title/description 내용 오류: {item_id}")
        if parser.meta.get("og:title") != full_page_name or parser.meta.get("og:description") != page_description:
            errors.append(f"아이템 Open Graph 내용 오류: {item_id}")
        if parser.meta.get("og:url") != expected:
            errors.append(f"아이템 og:url 오류: {item_id}")
        json_ld_rows = [body for script_type, body in parser.scripts if script_type == "application/ld+json"]
        try:
            structured = json.loads(json_ld_rows[0]) if json_ld_rows else {}
        except json.JSONDecodeError as exc:
            errors.append(f"아이템 JSON-LD 오류: {item_id}: {exc}")
            structured = {}
        if structured.get("@type") != "ItemPage" or structured.get("name") != full_page_name or structured.get("url") != expected or structured.get("inLanguage") != "ko-KR":
            errors.append(f"아이템 JSON-LD 계약 오류: {item_id}")
        text = " ".join(parser.text)
        for marker in ["하위 조합 재료", "현재 아이템", "상위 업그레이드", f"아이템 ID {item_id}", "총 가격", "조합 비용", "구매"] + LEGAL_MARKERS:
            if marker not in text:
                errors.append(f"아이템 상세 표식 '{marker}' 없음: {item_id}")
        if not entry.get("from") and "기본 아이템" not in text:
            errors.append(f"기본 아이템 상태 없음: {item_id}")
        if not entry.get("into") and "상위 업그레이드 없음" not in text:
            errors.append(f"최종 아이템 상태 없음: {item_id}")
        gold_value = entry.get("gold")
        gold: dict[str, object] = gold_value if isinstance(gold_value, dict) else {}
        current_markers = [
            str(entry.get("name", "이름 없음")),
            f"총 가격 {gold.get('total', '데이터 없음')}",
            f"조합 비용 {gold.get('base', '데이터 없음')}",
            f"구매 {expected_purchase(entry)}",
            *expected_badges(entry),
        ]
        for marker in current_markers:
            if marker not in text: errors.append(f"아이템 현재 노드 데이터 '{marker}' 불일치: {item_id}")
        for relation_key in ("from", "into"):
            counts = Counter(str(ref) for ref in refs_for(entry, relation_key))
            for ref_id, quantity in counts.items():
                target = items[ref_id]
                target_gold_value = target.get("gold")
                target_gold: dict[str, object] = target_gold_value if isinstance(target_gold_value, dict) else {}
                relation_markers = [
                    str(target.get("name", "이름 없음")),
                    f"아이템 ID {ref_id}",
                    f"총 가격 {target_gold.get('total', '데이터 없음')}",
                    f"조합 비용 {target_gold.get('base', '데이터 없음')}",
                    f"구매 {expected_purchase(target)}",
                    *expected_badges(target),
                ]
                if quantity > 1:
                    relation_markers.append(f"×{quantity}")
                for marker in relation_markers:
                    if marker not in text: errors.append(f"아이템 {relation_key} 노드 데이터 '{marker}' 불일치: {item_id}->{ref_id}")
        expected_labels = [expected_node_label(entry, item_id)]
        expected_labels.extend(expected_relation_labels(refs_for(entry, "from"), items, "from", visited=frozenset({item_id})))
        expected_labels.extend(expected_relation_labels(refs_for(entry, "into"), items, "into", visited=frozenset({item_id})))
        if Counter(parser.item_node_labels) != Counter(expected_labels):
            errors.append(f"아이템 재귀 노드 내용·수량 불일치: {item_id}")
        for image in parser.images:
            expected_prefix = f"{BASE}/assets/riot-data-dragon/{VERSION}/img/item/"
            if not image.startswith(expected_prefix) or not public_file(urlparse(image).path).is_file():
                errors.append(f"아이템 상세 이미지 오류: {item_id} -> {image}")
        for link in parser.links:
            parsed = urlparse(link)
            if parsed.scheme or parsed.netloc or not parsed.path.startswith(BASE):
                continue
            relative = parsed.path.removeprefix(BASE) or "/"
            target = file_for(relative) if relative.endswith("/") else SITE/relative.lstrip("/")
            if not target.exists():
                errors.append(f"아이템 상세 깨진 내부 링크: {item_id} -> {link}")

    duplicate_page = (SITE/"season3-items/3028/index.html").read_text(encoding="utf-8")
    if "×2" not in duplicate_page or duplicate_page.count("아이템 ID 1004") < 1:
        errors.append("동일 재료 수량 집계 회귀: 3028에서 1004 ×2 없음")
    item_list_source = (SITE/"season3-items/index.html").read_text(encoding="utf-8")
    if item_list_source.count('data-item-search=') != EXPECTED_ITEM_DETAIL_PAGES or "item-search.js" not in item_list_source:
        errors.append("아이템 목록 검색·상세 진입 링크 오류")

    sitemap = (SITE/"sitemap.xml").read_text(encoding="utf-8") if (SITE/"sitemap.xml").exists() else ""
    for url in expected_canonicals:
        if f"<loc>{url}</loc>" not in sitemap: errors.append(f"사이트맵 URL 없음: {url}")
    robots = (SITE/"robots.txt").read_text(encoding="utf-8") if (SITE/"robots.txt").exists() else ""
    if "Allow: /" not in robots or f"Sitemap: https://ai-worker-lab.github.io{BASE}/sitemap.xml" not in robots: errors.append("robots.txt 규칙 오류")
    builder = (SITE/"assets/builder.js").read_text(encoding="utf-8") if (SITE/"assets/builder.js").exists() else ""
    for token in ["localStorage.getItem","localStorage.setItem","remove"]:
        if token not in builder: errors.append(f"빌더 동작 토큰 없음: {token}")
    item_search = (SITE/"assets/item-search.js").read_text(encoding="utf-8") if (SITE/"assets/item-search.js").exists() else ""
    for token in ["itemSearch", "addEventListener('input'", "hidden"]:
        if token not in item_search: errors.append(f"아이템 검색 동작 토큰 없음: {token}")
    site_css = (SITE/"assets/site.css").read_text(encoding="utf-8") if (SITE/"assets/site.css").exists() else ""
    for token in [":focus-visible", "grid-template-columns:repeat(3", "@media(max-width:820px)", ".tree-stage-current{order:2}"]:
        if token not in site_css: errors.append(f"아이템 반응형·키보드 스타일 토큰 없음: {token}")

    deployed_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in SITE.rglob("*") if path.is_file() and path.suffix in {".html",".js",".json",".css"})
    if re.search(r"(?:api[_-]?key|secret|password)\s*[:=]", deployed_text, re.I): errors.append("배포 산출물에서 비밀정보 형태 문자열 감지")
    if re.search(r"(?:adsbygoogle|paypal|stripe|patreon|buymeacoffee)", deployed_text, re.I): errors.append("수익화 코드 감지")

    if errors:
        print("검증 실패")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"검증 성공: 기본 페이지 {len(REQUIRED_PATHS)}개 + 아이템 상세 {EXPECTED_ITEM_DETAIL_PAGES}개, 오류 0건")
    print("데이터 항목:", ", ".join(f"{key}={value}" for key,value in manifest["counts"].items()))
    print(f"이미지: 참조 {len(asset_refs)}개, 고유 파일 {len(manifest_images)}개, vendor/site 누락·추가 0")
    print("정책: 필수 고지·비수익화·공식 이미지 경로·Riot 로고 미사용 확인")
    print("SEO: canonical/description/Open Graph/JSON-LD/robots/sitemap 확인")
    print(f"아이템 관계: from 보유/into 보유 {from_items}/{into_items}, 참조 {from_refs}/{into_refs}, 누락·순환·깨진 링크 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
