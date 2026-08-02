#!/usr/bin/env python3
"""검증된 Riot Data Dragon 시즌 3 역사 자료로 정적 사이트를 생성한다."""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
VERSION = "3.13.24"
LOCALE = "ko_KR"
CHECKED_AT = "2026-08-02"
ORIGIN = "https://ai-worker-lab.github.io"
BASE = "/lol-classic-hub"
SITE_URL = f"{ORIGIN}{BASE}"
DATA_ROOT = ROOT / "assets/upstream" / VERSION / "data" / LOCALE
IMAGE_ROOT = ROOT / "assets/vendor/riot-data-dragon" / VERSION / "img"
PUBLIC_IMAGE_ROOT = SITE / "assets/riot-data-dragon" / VERSION / "img"
CDN_DATA = f"https://ddragon.leagueoflegends.com/cdn/{VERSION}/data/{LOCALE}"

SOURCES = {
    "champions": f"{CDN_DATA}/champion.json",
    "items": f"{CDN_DATA}/item.json",
    "masteries": f"{CDN_DATA}/mastery.json",
    "runes": f"{CDN_DATA}/rune.json",
}
DATA_FILES = {
    "champions": "champion.json",
    "items": "item.json",
    "masteries": "mastery.json",
    "runes": "rune.json",
}
IMAGE_KINDS = {
    "champions": "champion",
    "items": "item",
    "masteries": "mastery",
    "runes": "rune",
}
EXPECTED_COUNTS = {"champions": 116, "items": 205, "masteries": 56, "runes": 296}
OFFICIAL_DATA_SHA256 = {
    "champions": "d073d5a023cb700118c3d63652b15d11fb8e213896897828cc024daef0cea925",
    "items": "cecc6ed683f80f076f0888053648f9604017155a9f9cc3ad2d9b47c3f8254bbe",
    "masteries": "2fd552d4fbf4cb25b5b4e1ba6e7bd7e7a3ba1dc1a63cbfe3fef34e57385a53ae",
    "runes": "de3d476f130bacd46e122acbc9a5a95fa2a1af94c8fce1d422297b1de795857f",
}
NAV = [
    ("/", "홈"),
    ("/runes/", "룬"),
    ("/masteries/", "특성"),
    ("/season3-items/", "아이템"),
    ("/champions/", "챔피언"),
    ("/builder/", "빌드 저장"),
]

CSS = r"""
:root{--bg:#0b1220;--panel:#111c30;--panel2:#17253d;--text:#eef3fb;--muted:#a9b7cc;--accent:#67e8c1;--gold:#f4c96b;--line:#2b3b55;--max:1180px;color-scheme:dark}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 80% 0,#183357 0,transparent 38%),var(--bg);color:var(--text);font-family:system-ui,-apple-system,"Noto Sans KR",sans-serif;line-height:1.62}a{color:var(--accent)}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:#fff;color:#000;padding:.6rem;z-index:9}.wrap{width:min(calc(100% - 2rem),var(--max));margin:auto}.site-header{border-bottom:1px solid var(--line);background:#0b1220e8;backdrop-filter:blur(12px);position:sticky;top:0;z-index:5}.header-inner{display:flex;align-items:center;justify-content:space-between;gap:1rem;min-height:64px}.brand{color:var(--text);text-decoration:none;font-weight:900;letter-spacing:-.03em}.brand span{color:var(--accent)}nav{display:flex;gap:.25rem;flex-wrap:wrap}nav a{color:var(--muted);text-decoration:none;padding:.45rem .62rem;border-radius:.5rem;font-size:.92rem}nav a:hover,nav a[aria-current=page]{color:var(--text);background:var(--panel2)}main{padding:3.5rem 0 5rem}.hero{padding:1.5rem 0 2rem}.eyebrow{color:var(--accent);font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:.78rem}h1{font-size:clamp(2.1rem,7vw,4.5rem);line-height:1.08;letter-spacing:-.055em;margin:.25rem 0 1rem;max-width:950px}h2{font-size:clamp(1.4rem,3vw,2rem);margin:2.5rem 0 .8rem;letter-spacing:-.025em}h3{margin:.2rem 0 .45rem}.lede{font-size:1.13rem;color:var(--muted);max-width:850px}.notice,.source,.legal{background:#172033;border:1px solid #3d526f;border-left:4px solid var(--gold);padding:1rem 1.15rem;border-radius:.65rem;margin:1.3rem 0}.notice strong,.source dt{color:var(--gold)}.source dl{display:grid;grid-template-columns:max-content 1fr;gap:.35rem 1rem}.source dd{margin:0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem}.card{display:block;background:linear-gradient(150deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:1rem;padding:1.2rem;color:var(--text);text-decoration:none}.card p{color:var(--muted)}.tag{display:inline-block;color:var(--accent);font-size:.77rem;font-weight:800;letter-spacing:.05em}.data-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:.85rem}.data-card{background:var(--panel);border:1px solid var(--line);border-radius:.8rem;padding:.9rem;display:grid;grid-template-columns:58px 1fr;gap:.85rem;min-height:118px}.data-card img{width:56px;height:56px;border-radius:.55rem;background:#07101e;image-rendering:auto}.data-card h3{font-size:1rem;line-height:1.35}.data-card p{grid-column:1/-1;color:var(--muted);font-size:.88rem;margin:.25rem 0 0}.data-card .meta{font-size:.78rem;color:var(--gold)}.count{color:var(--accent);font-weight:800}.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem}.form-grid .full{grid-column:1/-1}label{display:block;font-weight:700;margin-bottom:.35rem}input,textarea,button{font:inherit}input,textarea{width:100%;background:#08111f;color:var(--text);border:1px solid var(--line);border-radius:.55rem;padding:.7rem}textarea{min-height:90px}button,.button{background:var(--accent);color:#052019;border:0;border-radius:.55rem;padding:.7rem 1rem;font-weight:800}.saved article{border:1px solid var(--line);border-radius:.7rem;padding:1rem;margin:.7rem 0}.small{color:var(--muted);font-size:.85rem}footer{border-top:1px solid var(--line);padding:2rem 0 3rem;color:var(--muted);font-size:.84rem}footer p{margin:.45rem 0}.legal-title{color:var(--text);font-weight:800}@media(max-width:720px){.header-inner{align-items:flex-start;flex-direction:column;padding:.75rem 0}.form-grid{grid-template-columns:1fr}.source dl{display:block}.source dt{margin-top:.6rem}.data-grid{grid-template-columns:1fr}}
""".strip()

ITEM_TREE_CSS = r"""
:focus-visible{outline:3px solid var(--gold);outline-offset:3px}.item-search{margin:1rem 0 1.5rem}.item-search label{display:block;font-weight:800;margin-bottom:.4rem}.item-search input{width:min(100%,34rem);padding:.8rem 1rem;border:1px solid var(--line);border-radius:.65rem;background:var(--panel);color:var(--text);font:inherit}.item-list-link{color:inherit;text-decoration:none}.item-list-link:hover{border-color:var(--accent);transform:translateY(-2px)}.tree-breadcrumb{margin-bottom:1rem}.tree-layout{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;align-items:stretch}.tree-stage{min-width:0;height:100%;background:#0e192b;border:1px solid var(--line);border-radius:1rem;padding:1rem}.tree-stage h2{font-size:1.25rem;margin:0 0 .35rem}.stage-kicker{display:block;color:var(--accent);font-size:.78rem;font-weight:800;letter-spacing:.07em}.item-tree{list-style:none;margin:.8rem 0 0;padding:0}.item-tree .item-tree{margin-left:1rem;padding-left:.8rem;border-left:2px solid var(--line)}.item-tree li{margin:.65rem 0}.item-node{display:flex;gap:.8rem;align-items:flex-start;width:100%;min-width:0;padding:.75rem;background:linear-gradient(150deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:.8rem;color:var(--text);text-decoration:none}.item-node:hover{border-color:var(--accent)}.current-item{border-color:var(--gold);box-shadow:0 0 0 1px #f4c96b33}.item-node img{flex:0 0 auto;border-radius:.45rem}.item-node-copy{display:flex;flex-wrap:wrap;gap:.15rem .45rem;min-width:0}.item-node-copy strong{width:100%;overflow-wrap:anywhere}.item-id,.item-cost,.item-purchase{display:block;width:100%;color:var(--muted);font-size:.82rem}.quantity{color:var(--gold);font-weight:900}.item-badges{display:flex;flex-wrap:wrap;gap:.3rem}.item-badge{font-size:.72rem;border:1px solid #6d557c;background:#362941;color:#f0d9ff;border-radius:999px;padding:.08rem .4rem}.tree-state{color:var(--muted);border:1px dashed var(--line);border-radius:.65rem;padding:.7rem}.tree-description{max-width:780px}.search-empty{display:none;color:var(--muted)}
@media(max-width:820px){.tree-layout{grid-template-columns:1fr}.tree-stage-materials{order:1}.tree-stage-current{order:2}.tree-stage-upgrades{order:3}.item-tree .item-tree{margin-left:.5rem}.header-inner{align-items:flex-start;padding:.65rem 0}}
""".strip()

ITEM_SEARCH_JS = r"""
(() => {
  const input = document.querySelector('#item-search');
  const cards = [...document.querySelectorAll('[data-item-search]')];
  const empty = document.querySelector('#item-search-empty');
  if (!input || !cards.length) return;
  const filter = () => {
    const query = input.value.trim().toLocaleLowerCase('ko-KR');
    let visible = 0;
    cards.forEach(card => { const show = !query || card.dataset.itemSearch.toLocaleLowerCase('ko-KR').includes(query); card.hidden = !show; if (show) visible += 1; });
    if (empty) empty.style.display = visible ? 'none' : 'block';
  };
  input.addEventListener('input', filter);
})();
""".strip()

BUILDER_JS = r"""
(() => {
  const KEY = 'classic-notes-builds-v1';
  const form = document.querySelector('#build-form');
  const list = document.querySelector('#saved-builds');
  const status = document.querySelector('#save-status');
  const read = () => { try { const v = JSON.parse(localStorage.getItem(KEY) || '[]'); return Array.isArray(v) ? v.filter(x => x && typeof x === 'object') : []; } catch { return []; } };
  const write = builds => localStorage.setItem(KEY, JSON.stringify(builds));
  const clean = value => String(value || '').trim();
  const render = () => { const builds = read(); list.replaceChildren(); if (!builds.length) { const p = document.createElement('p'); p.className = 'small'; p.textContent = '아직 저장한 빌드가 없습니다.'; list.append(p); return; } builds.forEach(build => { const article=document.createElement('article'); const title=document.createElement('h3'); title.textContent=build.name||'이름 없는 빌드'; const detail=document.createElement('p'); detail.textContent=`챔피언: ${build.champion||'-'} / 룬: ${build.runes||'-'} / 특성: ${build.masteries||'-'} / 아이템: ${build.items||'-'}`; const remove=document.createElement('button'); remove.type='button'; remove.textContent='삭제'; remove.dataset.id=build.id; article.append(title,detail,remove); list.append(article); }); };
  form.addEventListener('submit', event => { event.preventDefault(); const data=new FormData(form); const build={id:crypto.randomUUID?crypto.randomUUID():String(Date.now()),name:clean(data.get('name')),champion:clean(data.get('champion')),runes:clean(data.get('runes')),masteries:clean(data.get('masteries')),items:clean(data.get('items')),updatedAt:new Date().toISOString()}; const builds=read(); builds.unshift(build); write(builds.slice(0,30)); form.reset(); status.textContent='이 브라우저에 저장했습니다.'; render(); });
  list.addEventListener('click', event => { const id=event.target.dataset.id; if (!id) return; write(read().filter(build => build.id !== id)); status.textContent='저장 항목을 삭제했습니다.'; render(); });
  render();
})();
""".strip()


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def plain(value: object) -> str:
    if isinstance(value, list):
        value = " ".join(str(part) for part in value)
    parser = TextExtractor()
    parser.feed(str(value or ""))
    return re.sub(r"\s+", " ", " ".join(parser.parts)).strip()


def href(path: str) -> str:
    return f"{BASE}{path}"


def canonical(path: str) -> str:
    return f"{SITE_URL}{path}"


def validate_item_id(item_id: str) -> str:
    if not re.fullmatch(r"[0-9]+", item_id):
        raise ValueError(f"안전하지 않은 아이템 ID: {item_id!r}")
    return item_id


def validate_asset_filename(filename: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", filename) or filename in {".", ".."} or ".." in Path(filename).parts:
        raise ValueError(f"안전하지 않은 이미지 파일명: {filename!r}")
    return filename


def legal_footer() -> str:
    return """<p class="legal-title">비공식 개인 팬 프로젝트 · 광고·결제·후원·유료 기능 없음</p>
<p>클래식 노트 isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.</p>
<p>클래식 노트 was created under Riot Games' "Legal Jibber Jabber" policy using assets owned by Riot Games. Riot Games does not endorse or sponsor this project.</p>
<p>Data Dragon 3.13.24/ko_KR · 확인일 2026-08-02 · 2026 League Classic 현행 데이터와 동일함을 보증하지 않습니다.</p>"""


def layout(path: str, title: str, description: str, body: str, kind: str = "WebPage", robots: str = "index,follow,max-image-preview:large") -> str:
    current = next((label for target, label in NAV if target == path), "")
    if path.startswith("/season3-items/"):
        current = "아이템"
    nav = "".join(f'<a href="{href(target)}"' + (' aria-current="page"' if label == current else "") + f'>{label}</a>' for target, label in NAV)
    structured = {"@context":"https://schema.org","@type":kind,"name":title,"description":description,"url":canonical(path),"inLanguage":"ko-KR","isPartOf":{"@type":"WebSite","name":"클래식 노트","url":f"{SITE_URL}/"}}
    json_ld = json.dumps(structured, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(description, quote=True)}"><meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical(path)}"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="클래식 노트"><meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(description, quote=True)}"><meta property="og:url" content="{canonical(path)}"><meta name="twitter:card" content="summary"><link rel="stylesheet" href="{href('/assets/site.css')}"><script type="application/ld+json">{json_ld}</script></head>
<body><a class="skip" href="#content">본문으로 이동</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{href('/')}">클래식 <span>노트</span></a><nav aria-label="주요 메뉴">{nav}</nav></div></header><main id="content" class="wrap">{body}</main><footer><div class="wrap">{legal_footer()}</div></footer></body></html>"""


def load_datasets() -> tuple[dict[str, list[dict[str, object]]], dict[str, str]]:
    datasets: dict[str, list[dict[str, object]]] = {}
    hashes: dict[str, str] = {}
    for key, filename in DATA_FILES.items():
        path = DATA_ROOT / filename
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != OFFICIAL_DATA_SHA256[key]:
            raise ValueError(f"{key} 공식 데이터 SHA-256 불일치: {digest}")
        payload = json.loads(raw)
        values = []
        for entry_id, source_entry in payload["data"].items():
            entry = dict(source_entry)
            entry["_id"] = validate_item_id(str(entry_id)) if key == "items" else str(entry_id)
            values.append(entry)
        if len(values) != EXPECTED_COUNTS[key]:
            raise ValueError(f"{key} 개수 오류: {len(values)} != {EXPECTED_COUNTS[key]}")
        datasets[key] = values
        hashes[key] = digest
    return datasets, hashes


def image_src(kind: str, entry: dict[str, object]) -> str:
    image_value = entry.get("image")
    image: dict[str, object] = image_value if isinstance(image_value, dict) else {}
    filename = validate_asset_filename(str(image.get("full", "")))
    return html.escape(href(f"/assets/riot-data-dragon/{VERSION}/img/{kind}/{filename}"), quote=True)


def aggregate_refs(refs: list[object]) -> list[tuple[str, int]]:
    """형제 참조를 최초 등장 순서대로 집계한다."""
    normalized = [str(ref) for ref in refs]
    counts = Counter(normalized)
    return [(ref, counts[ref]) for ref in dict.fromkeys(normalized)]


def item_badges(entry: dict[str, object]) -> list[str]:
    """공식 데이터에 명시된 구매·맵 제한만 배지 문구로 반환한다."""
    badges: list[str] = []
    gold = entry.get("gold")
    purchasable = entry.get("purchasable")
    if purchasable is None and isinstance(gold, dict):
        purchasable = gold.get("purchasable")
    if purchasable is False:
        badges.append("구매 불가")
    maps = entry.get("maps")
    if isinstance(maps, dict):
        excluded = [str(map_id) for map_id, available in maps.items() if available is False]
        included = [str(map_id) for map_id, available in maps.items() if available is True]
        badges.extend(f"맵 {map_id} 제외" for map_id in excluded)
        if included and not excluded:
            badges.append("맵 " + ", ".join(included) + " 전용")
    return badges


def render_item_node(entry: dict[str, object], quantity: int = 1, current: bool = False) -> str:
    item_id = html.escape(str(entry.get("_id", "알 수 없음")))
    name = html.escape(str(entry.get("name", "이름 없음")))
    gold_value = entry.get("gold")
    gold: dict[str, object] = gold_value if isinstance(gold_value, dict) else {}
    total = html.escape(str(gold.get("total", "데이터 없음")))
    base = html.escape(str(gold.get("base", "데이터 없음")))
    purchasable_value = entry.get("purchasable")
    if purchasable_value is None:
        purchasable_value = gold.get("purchasable")
    purchasable = "가능" if purchasable_value is True else "불가" if purchasable_value is False else "데이터 없음"
    quantity_accessible = f" {quantity}개 필요" if quantity > 1 else ""
    quantity_html = f'<span class="quantity" aria-label="{quantity}개 필요">×{quantity}</span>' if quantity > 1 else ""
    badge_labels = item_badges(entry)
    badges = "".join(f'<span class="item-badge">{html.escape(label)}</span>' for label in badge_labels)
    badge_accessible = " 배지: " + ", ".join(badge_labels) if badge_labels else ""
    content = f'''<img src="{image_src("item", entry)}" alt="" width="56" height="56" loading="lazy"><span class="item-node-copy"><strong>{name}</strong>{quantity_html}<span class="item-id">아이템 ID {item_id}</span><span class="item-cost">총 가격 {total} · 조합 비용 {base}</span><span class="item-purchase">구매 {purchasable}</span><span class="item-badges">{badges}</span></span>'''
    title = f"아이템 {item_id} 조합·업그레이드 트리 보기"
    accessible_label = (
        f"{name}{quantity_accessible} 아이템 ID {item_id} "
        f"총 가격 {total} · 조합 비용 {base} 구매 {purchasable}{badge_accessible}"
    )
    if current:
        return f'<div class="item-node current-item" aria-current="true" aria-label="{html.escape(accessible_label, quote=True)}">{content}</div>'
    return f'<a class="item-node" href="{href(f"/season3-items/{item_id}/")}" title="{html.escape(title, quote=True)}" aria-label="{html.escape(accessible_label, quote=True)}">{content}</a>'


def render_relation_tree(
    refs: list[object],
    items: dict[str, dict[str, object]],
    relation_key: str,
    *,
    visited: frozenset[str] = frozenset(),
    depth: int = 0,
    max_depth: int = 8,
) -> str:
    """관계 트리를 누락·순환·깊이 제한에 안전하게 렌더링한다."""
    if depth >= max_depth:
        return '<p class="tree-state">최대 깊이 도달</p>'
    nodes: list[str] = []
    for item_id, quantity in aggregate_refs(refs):
        if item_id in visited:
            nodes.append(f'<li class="tree-state">아이템 ID {html.escape(item_id)} · 순환 관계 중단</li>')
            continue
        entry = items.get(item_id)
        if entry is None:
            nodes.append(f'<li class="tree-state">아이템 ID {html.escape(item_id)} · 데이터 없음</li>')
            continue
        children = entry.get(relation_key)
        subtree = ""
        if isinstance(children, list) and children:
            subtree = render_relation_tree(children, items, relation_key, visited=visited | {item_id}, depth=depth + 1, max_depth=max_depth)
        nodes.append(f'<li>{render_item_node(entry, quantity)}{subtree}</li>')
    return '<ul class="item-tree">' + "".join(nodes) + "</ul>"


def render_item_detail(entry: dict[str, object], items: dict[str, dict[str, object]]) -> str:
    item_id = str(entry.get("_id", ""))
    from_value = entry.get("from")
    into_value = entry.get("into")
    from_refs = from_value if isinstance(from_value, list) else []
    into_refs = into_value if isinstance(into_value, list) else []
    materials = render_relation_tree(from_refs, items, "from", visited=frozenset({item_id})) if from_refs else '<p class="tree-state">기본 아이템</p>'
    upgrades = render_relation_tree(into_refs, items, "into", visited=frozenset({item_id})) if into_refs else '<p class="tree-state">상위 업그레이드 없음</p>'
    return f'''<div class="tree-layout" role="group" aria-label="아이템 조합 및 업그레이드 단계">
<section class="tree-stage tree-stage-materials" aria-labelledby="materials-title"><span class="stage-kicker">1단계</span><h2 id="materials-title">하위 조합 재료</h2><p class="small">이 아이템을 만드는 데 필요한 재료입니다.</p>{materials}</section>
<section class="tree-stage tree-stage-current" aria-labelledby="current-title"><span class="stage-kicker">2단계</span><h2 id="current-title">현재 아이템</h2>{render_item_node(entry, current=True)}</section>
<section class="tree-stage tree-stage-upgrades" aria-labelledby="upgrades-title"><span class="stage-kicker">3단계</span><h2 id="upgrades-title">상위 업그레이드</h2><p class="small">이 아이템에서 올라갈 수 있는 아이템입니다.</p>{upgrades}</section>
</div>'''


def entry_detail(key: str, entry: dict[str, object]) -> tuple[str, str]:
    if key == "champions":
        tags = ", ".join(str(x) for x in entry.get("tags", []))
        stats = entry.get("stats") or {}
        detail = f"역할 {tags or '-'} · 기본 체력 {stats.get('hp', '-')} · 공격력 {stats.get('attackdamage', '-')}"
        return detail, "시즌 3 역사 챔피언 데이터"
    if key == "items":
        gold = entry.get("gold") or {}
        detail = plain(entry.get("plaintext") or entry.get("description"))
        return detail, f"총 가격 {gold.get('total', '-')} 골드"
    if key == "runes":
        return plain(entry.get("description")), "시즌 3 룬"
    descriptions = entry.get("description") or []
    return plain(descriptions), "시즌 3 특성(마스터리)"


def data_cards(key: str, values: list[dict[str, object]]) -> str:
    kind = IMAGE_KINDS[key]
    sorted_values = sorted(values, key=lambda value: str(value.get("name", "")))
    cards: list[str] = []
    for entry in sorted_values:
        name = html.escape(str(entry.get("name", "이름 없음")))
        image = entry.get("image") or {}
        filename = str(image.get("full", ""))
        local = IMAGE_ROOT / kind / filename
        if not filename or not local.is_file():
            raise FileNotFoundError(f"공식 이미지 없음: {key}/{filename}")
        detail, meta = entry_detail(key, entry)
        card_body = f'<img src="{image_src(kind, entry)}" alt="{name} 아이콘" width="56" height="56" loading="lazy"><div><h3>{name}</h3><div class="meta">{html.escape(meta)}</div></div><p>{html.escape(detail) or "설명 없음"}</p>'
        if key == "items":
            item_id = html.escape(str(entry.get("_id", "")))
            cards.append(f'<a class="data-card item-list-link" data-item-search="{name} {item_id}" href="{href(f"/season3-items/{item_id}/")}" title="{name} 상세 트리 보기">{card_body}</a>')
        else:
            cards.append(f'<article class="data-card">{card_body}</article>')
    return '<div class="data-grid">' + "".join(cards) + "</div>"


def source_box(label: str, key: str, count: int) -> str:
    url = SOURCES[key]
    return f"""<aside class="source" aria-label="데이터 출처"><h2>출처와 검증 상태</h2><dl>
<dt>대상 데이터</dt><dd>{html.escape(label)} <span class="count">{count}개</span></dd>
<dt>공식 출처</dt><dd><a href="{url}" rel="nofollow external">Riot Games Data Dragon {VERSION}/{LOCALE} JSON</a></dd>
<dt>확인일</dt><dd><time datetime="{CHECKED_AT}">{CHECKED_AT}</time></dd>
<dt>적용 범위</dt><dd>시즌 3 역사 스냅샷. 2026 League Classic 현행 목록·수치와 동일함을 보증하지 않습니다.</dd>
</dl></aside>"""


def write_page(path: str, content: str) -> None:
    destination = SITE / path.lstrip("/") / "index.html" if path != "/" else SITE / "index.html"
    site_root = SITE.resolve()
    resolved_destination = destination.resolve()
    if not resolved_destination.is_relative_to(site_root):
        raise ValueError(f"site 밖의 출력 경로 거부: {path!r}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def main() -> None:
    datasets, hashes = load_datasets()
    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "assets").mkdir(parents=True)
    (SITE / "assets/site.css").write_text(CSS + "\n" + ITEM_TREE_CSS + "\n", encoding="utf-8")
    (SITE / "assets/builder.js").write_text(BUILDER_JS + "\n", encoding="utf-8")
    (SITE / "assets/item-search.js").write_text(ITEM_SEARCH_JS + "\n", encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    shutil.copytree(IMAGE_ROOT, PUBLIC_IMAGE_ROOT)

    total = sum(len(values) for values in datasets.values())
    home_body = f"""<section class="hero"><p class="eyebrow">공식 역사 데이터 공개</p><h1>기억 대신 출처로 확인하는<br>클래식 게임 정보 노트</h1><p class="lede">Riot Games Data Dragon {VERSION}/{LOCALE}에서 확인한 챔피언·아이템·룬·특성 {total}개와 공식 아이콘을 제공합니다.</p><div class="notice"><strong>정확성 안내</strong> 이 자료는 시즌 3 역사 스냅샷입니다. 2026 League Classic은 단일 역사 패치의 완전 복제가 아니므로 현행 게임 목록·수치와 동일하다고 단정하지 않습니다.</div><div class="legal"><strong>비공식 팬 프로젝트</strong> Riot Games 또는 League of Legends의 공식 서비스가 아니며 Riot 로고를 사용하지 않습니다. 광고·결제·후원·유료 기능이 없습니다.</div></section>
<section><h2>주제별 빠른 탐색</h2><div class="grid">
<a class="card" href="{href('/runes/')}"><span class="tag">296개</span><h3>룬 레퍼런스</h3><p>시즌 3 룬 이름·효과·아이콘</p></a>
<a class="card" href="{href('/masteries/')}"><span class="tag">56개</span><h3>특성(마스터리)</h3><p>공식 아이콘과 효과 설명</p></a>
<a class="card" href="{href('/season3-items/')}"><span class="tag">205개</span><h3>아이템 레퍼런스</h3><p>이름·설명·가격·아이콘</p></a>
<a class="card" href="{href('/champions/')}"><span class="tag">116개</span><h3>챔피언 레퍼런스</h3><p>시즌 3 역사 목록과 기본 능력치</p></a>
<a class="card" href="{href('/builder/')}"><span class="tag">브라우저 전용</span><h3>빌드 메모 저장</h3><p>계정 없이 이 브라우저에 빌드를 저장</p></a></div></section>"""
    write_page("/", layout("/", "클래식 노트 | 시즌 3 데이터 기록관", "Data Dragon 3.13.24의 2013 시즌 챔피언, 아이템, 룬, 특성을 공식 출처와 함께 확인하세요.", home_body, "WebSite"))

    refs = [
        ("/runes/", "시즌3 룬 레퍼런스", "runes", "룬"),
        ("/masteries/", "시즌3 특성·마스터리", "masteries", "특성"),
        ("/season3-items/", "시즌3 아이템 레퍼런스", "items", "아이템"),
        ("/champions/", "시즌3 챔피언 레퍼런스", "champions", "챔피언"),
    ]
    for path, title, key, noun in refs:
        values = datasets[key]
        search = f'''<div class="item-search"><label for="item-search">아이템 이름 또는 ID 검색</label><input id="item-search" type="search" autocomplete="off" placeholder="예: 조화의 성배 또는 3028"><p id="item-search-empty" class="search-empty" role="status">일치하는 아이템이 없습니다.</p></div>''' if key == "items" else ""
        script = f'<script src="{href("/assets/item-search.js")}" defer></script>' if key == "items" else ""
        body = f'<section class="hero"><p class="eyebrow">Data Dragon {VERSION}</p><h1>{title}</h1><p class="lede">공식 {LOCALE} 역사 데이터와 아이콘을 그대로 확인합니다. 현행 League Classic 동일성은 보증하지 않습니다.</p></section>{source_box(title, key, len(values))}<section><h2>{noun} 데이터</h2>{search}{data_cards(key, values)}</section>{script}'
        write_page(path, layout(path, f"{title} | 클래식 노트", f"Riot Games Data Dragon {VERSION}/{LOCALE} 공식 {noun} 역사 데이터와 아이콘.", body, "CollectionPage"))

    item_index = {str(entry["_id"]): entry for entry in datasets["items"]}
    for item_id, entry in item_index.items():
        name = str(entry.get("name", "이름 없음"))
        description = plain(entry.get("plaintext") or entry.get("description"))
        path = f"/season3-items/{item_id}/"
        body = f'''<p class="tree-breadcrumb"><a href="{href('/season3-items/')}">아이템 목록</a> / 아이템 ID {html.escape(item_id)}</p><section class="hero"><p class="eyebrow">Data Dragon {VERSION} · 아이템 {html.escape(item_id)}</p><h1>{html.escape(name)}</h1><p class="lede tree-description">{html.escape(description) or "설명 없음"}</p></section>{render_item_detail(entry, item_index)}'''
        write_page(path, layout(path, f"{name} 조합·업그레이드 트리 | 클래식 노트", f"{name}의 시즌 3 하위 조합 재료, 가격, 상위 업그레이드 트리.", body, "ItemPage"))

    builder_body = f"""<section class="hero"><p class="eyebrow">클라이언트 전용 도구</p><h1>클래식 빌드 메모</h1><p class="lede">계정 없이 이 브라우저에 룬·특성·아이템 메모를 저장하세요. 입력 내용은 서버로 전송되지 않습니다.</p></section><section><h2>새 빌드 저장</h2><form id="build-form" class="form-grid"><div><label for="name">빌드 이름</label><input id="name" name="name" required maxlength="80"></div><div><label for="champion">챔피언</label><input id="champion" name="champion" maxlength="80"></div><div class="full"><label for="runes">룬</label><textarea id="runes" name="runes" maxlength="500"></textarea></div><div class="full"><label for="masteries">특성</label><textarea id="masteries" name="masteries" maxlength="500"></textarea></div><div class="full"><label for="items">아이템</label><textarea id="items" name="items" maxlength="500"></textarea></div><div class="full"><button type="submit">이 브라우저에 저장</button> <span id="save-status" role="status" aria-live="polite"></span></div></form></section><section><h2>저장한 빌드</h2><div id="saved-builds" class="saved"></div><p class="small">브라우저 데이터 삭제 시 저장 내용도 사라집니다. 최대 30개를 보관합니다.</p></section><script src="{href('/assets/builder.js')}" defer></script>"""
    write_page("/builder/", layout("/builder/", "클래식 노트 빌드 저장 도구 | 브라우저 전용", "시즌 3 빌드 메모를 계정 없이 브라우저에 저장하는 클라이언트 전용 도구입니다.", builder_body, "SoftwareApplication"))

    not_found = f'''<section class="hero"><p class="eyebrow">404</p><h1>페이지를 찾을 수 없습니다</h1><p><a class="button" href="{href('/')}">홈으로 돌아가기</a></p></section>'''
    (SITE / "404.html").write_text(layout("/404.html", "페이지를 찾을 수 없습니다 | 클래식 노트", "요청한 페이지를 찾을 수 없습니다.", not_found, robots="noindex,follow"), encoding="utf-8")
    urls = [path for path, _ in NAV] + [f"/season3-items/{item_id}/" for item_id in item_index]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{canonical(path)}</loc><lastmod>{CHECKED_AT}</lastmod></url>\n" for path in urls) + "</urlset>\n"
    (SITE / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    unique_images = len({path.name + ':' + path.parent.name for path in IMAGE_ROOT.rglob("*.png")})
    manifest = {"generatedAt":CHECKED_AT,"sourceVersion":VERSION,"locale":LOCALE,"checkedAt":CHECKED_AT,"publicDistribution":True,"counts":{key:len(value) for key,value in datasets.items()},"uniqueImages":unique_images,"dataSha256":hashes,"sources":SOURCES,"limitations":["시즌 3 역사 스냅샷","2026 League Classic 현행 동일성 미보증","마스터리 트리 배경·연결선 제외"]}
    (SITE / "data-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
