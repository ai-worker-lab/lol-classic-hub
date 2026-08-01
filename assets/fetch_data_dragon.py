#!/usr/bin/env python3
"""Riot 공식 Data Dragon 3.13.24 이미지와 매니페스트를 재현한다."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import shutil
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

VERSION = "3.13.24"
LOCALE = "en_US"
KINDS = ("champion", "item", "rune", "mastery")
ROOT = Path(__file__).resolve().parent
BASE = "https://ddragon.leagueoflegends.com"
VERSION_LIST_URL = f"{BASE}/api/versions.json"
DOCS_URL = "https://developer.riotgames.com/docs/lol#data-dragon"
GENERAL_POLICY_URL = "https://developer.riotgames.com/policies/general"
LEGAL_URL = "https://www.riotgames.com/en/legal"
POLICY_REVIEWED_AT = "2026-08-02"
PUBLIC_POLICY_STATUS = "공개 가능 (조건부)"
USER_AGENT = "lol-classic-hub-asset-audit/1.0"


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def write_bytes_atomic(path: Path, body: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(body)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def sha256(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def download_image(job: dict[str, Any]) -> dict[str, Any]:
    try:
        body = fetch(job["original_url"])
    except urllib.error.HTTPError as error:
        return {
            **job,
            "availability": "unavailable",
            "http_status": error.code,
            "policy_status": "공식 URL 오류로 공개 대상 제외",
            "public_distribution": False,
            "reason": "공식 URL이 HTTP 오류를 반환함",
        }

    destination = ROOT / job["file"]
    write_bytes_atomic(destination, body)
    return {
        **job,
        "availability": "available",
        "http_status": 200,
        "sha256": sha256(body),
        "bytes": len(body),
        "policy_status": PUBLIC_POLICY_STATUS,
        "public_distribution": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--checked-at",
        required=True,
        help="확인 시각(UTC ISO 8601, 예: 2026-08-01T16:24:52Z)",
    )
    parser.add_argument("--workers", type=int, default=12)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.checked_at.endswith("Z"):
        raise SystemExit("--checked-at은 UTC Z 표기여야 합니다")

    upstream = ROOT / "upstream"
    source_data = upstream / VERSION / "data" / LOCALE
    vendor = ROOT / "vendor" / "riot-data-dragon" / VERSION
    if source_data.exists():
        shutil.rmtree(source_data)
    if vendor.exists():
        shutil.rmtree(vendor)

    versions_body = fetch(VERSION_LIST_URL)
    versions = json.loads(versions_body)
    season3_versions = [value for value in versions if value.startswith("3.")]
    if VERSION not in season3_versions:
        raise SystemExit(f"선택 버전 {VERSION}이 공식 버전 목록에 없습니다")
    write_bytes_atomic(upstream / "versions.json", versions_body)

    jobs: list[dict[str, Any]] = []
    datasets: list[dict[str, Any]] = []
    for kind in KINDS:
        data_url = f"{BASE}/cdn/{VERSION}/data/{LOCALE}/{kind}.json"
        data_body = fetch(data_url)
        document = json.loads(data_body)
        data_file = f"upstream/{VERSION}/data/{LOCALE}/{kind}.json"
        write_bytes_atomic(ROOT / data_file, data_body)
        datasets.append(
            {
                "kind": kind,
                "original_url": data_url,
                "version": VERSION,
                "locale": LOCALE,
                "checked_at": args.checked_at,
                "file": data_file,
                "sha256": sha256(data_body),
                "bytes": len(data_body),
                "entry_count": len(document["data"]),
                "availability": "available",
                "http_status": 200,
                "policy_status": PUBLIC_POLICY_STATUS,
                "public_distribution": True,
            }
        )
        for asset_id, record in sorted(document["data"].items()):
            filename = record["image"]["full"]
            jobs.append(
                {
                    "kind": kind,
                    "id": asset_id,
                    "name": record.get("name"),
                    "original_url": f"{BASE}/cdn/{VERSION}/img/{kind}/{filename}",
                    "version": VERSION,
                    "checked_at": args.checked_at,
                    "file": f"vendor/riot-data-dragon/{VERSION}/img/{kind}/{filename}",
                }
            )

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        assets = list(executor.map(download_image, jobs))
    assets.sort(key=lambda item: (item["kind"], str(item["id"])))

    unavailable = [item for item in assets if item["availability"] == "unavailable"]
    manifest = {
        "schema_version": 1,
        "generated_by": "assets/fetch_data_dragon.py",
        "checked_at": args.checked_at,
        "selection": {
            "selected_version": VERSION,
            "locale": LOCALE,
            "rationale_ko": (
                "공식 버전 목록에서 확인되는 3.x 아카이브 중 3.13 계열의 최종 빌드다. "
                "3.14 이상은 시즌 종료 뒤 프리시즌 변경을 포함할 가능성이 있어 보수적으로 제외했다."
            ),
            "official_version_list_url": VERSION_LIST_URL,
            "season3_accessible_versions": season3_versions,
        },
        "policy": {
            "status": PUBLIC_POLICY_STATUS,
            "public_distribution": True,
            "reviewed_at": POLICY_REVIEWED_AT,
            "note_ko": (
                "개인 비상업 팬 프로젝트, 두 필수 고지, 공식 출처·버전·확인일 표시, Riot 로고 미사용, "
                "비수익화 조건으로 공개한다. Developer Portal 제품 등록·감사는 AIW-184에서 병행한다. "
                "공식 아카이브 미제공 자산은 제외한다."
            ),
            "sources": [GENERAL_POLICY_URL, DOCS_URL, LEGAL_URL],
        },
        "datasets": datasets,
        "assets": assets,
        "unavailable": unavailable,
        "not_provided_by_archive": [
            {
                "kind": "mastery_tree_chrome",
                "availability": "unavailable",
                "policy_status": "공식 아카이브 미제공으로 공개 대상 제외",
                "public_distribution": False,
                "checked_at": args.checked_at,
                "reason_ko": (
                    "공식 3.13.24 mastery.json은 마스터리 아이콘과 트리 배치를 제공하지만 "
                    "트리 배경·연결선용 별도 파일 URL은 제공하지 않는다. 출처 불명 복제나 현대 자산 대체를 하지 않는다."
                ),
            }
        ],
        "summary": {
            "dataset_count": len(datasets),
            "asset_count": len(assets),
            "unique_image_file_count": len({item["file"] for item in assets}),
            "available_count": len(assets) - len(unavailable),
            "unavailable_count": len(unavailable) + 1,
            "not_provided_count": 1,
            "policy_pending_count": 0,
            "public_distribution_count": len(assets) - len(unavailable) + len(datasets),
            "excluded_from_distribution_count": len(unavailable) + 1,
        }
    }
    write_bytes_atomic(
        ROOT / "manifest.json",
        (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(),
    )
    print(json.dumps(manifest["summary"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
