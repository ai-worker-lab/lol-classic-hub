#!/usr/bin/env python3
"""Riot 공식 Data Dragon 역사 스냅샷으로 정적 MVP를 생성한다."""

from __future__ import annotations

import html
import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
VERSION = "3.15.5"
LOCALE = "ko_KR"
CHECKED_AT = "2026-08-02"
ORIGIN = "https://ai-worker-lab.github.io"
BASE = "/lol-classic-hub"
SITE_URL = f"{ORIGIN}{BASE}"
CDN = f"https://ddragon.leagueoflegends.com/cdn/{VERSION}/data/{LOCALE}"


SOURCES = {
    "champions": f"{CDN}/champion.json",
    "items": f"{CDN}/item.json",
    "masteries": f"{CDN}/mastery.json",
    "runes": f"{CDN}/rune.json",
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
:root{--bg:#0b1220;--panel:#111c30;--panel2:#17253d;--text:#eef3fb;--muted:#a9b7cc;--accent:#67e8c1;--gold:#f4c96b;--line:#2b3b55;--danger:#ffb4a8;--max:1120px;color-scheme:dark}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 80% 0,#183357 0,transparent 38%),var(--bg);color:var(--text);font-family:system-ui,-apple-system,"Noto Sans KR",sans-serif;line-height:1.65}a{color:var(--accent)}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:#fff;color:#000;padding:.6rem;z-index:9}.wrap{width:min(calc(100% - 2rem),var(--max));margin:auto}.site-header{border-bottom:1px solid var(--line);background:#0b1220e8;backdrop-filter:blur(12px);position:sticky;top:0;z-index:5}.header-inner{display:flex;align-items:center;justify-content:space-between;gap:1rem;min-height:64px}.brand{color:var(--text);text-decoration:none;font-weight:900;letter-spacing:-.03em}.brand span{color:var(--accent)}nav{display:flex;gap:.25rem;flex-wrap:wrap}nav a{color:var(--muted);text-decoration:none;padding:.45rem .62rem;border-radius:.5rem;font-size:.92rem}nav a:hover,nav a[aria-current=page]{color:var(--text);background:var(--panel2)}main{padding:3.5rem 0 5rem}.hero{padding:2rem 0 3rem}.eyebrow{color:var(--accent);font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:.78rem}h1{font-size:clamp(2.1rem,7vw,4.8rem);line-height:1.08;letter-spacing:-.055em;margin:.25rem 0 1rem;max-width:900px}h2{font-size:clamp(1.4rem,3vw,2rem);margin:2.5rem 0 .8rem;letter-spacing:-.025em}h3{margin:.2rem 0 .6rem}.lede{font-size:1.15rem;color:var(--muted);max-width:760px}.notice{background:#172033;border:1px solid #3d526f;border-left:4px solid var(--gold);padding:1rem 1.15rem;border-radius:.65rem;margin:1.3rem 0}.notice strong{color:var(--gold)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem}.card{display:block;background:linear-gradient(150deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:1rem;padding:1.25rem;color:var(--text);text-decoration:none;min-height:155px}.card:hover{border-color:var(--accent);transform:translateY(-2px)}.card p{color:var(--muted);margin:.5rem 0}.tag{display:inline-block;border:1px solid var(--line);border-radius:999px;color:var(--muted);font-size:.8rem;padding:.16rem .52rem}.source{background:var(--panel);border:1px solid var(--line);border-radius:.8rem;padding:1rem 1.2rem;margin:2.5rem 0}.source dl{display:grid;grid-template-columns:max-content 1fr;gap:.35rem 1rem;margin:.5rem 0}.source dt{color:var(--muted)}.source dd{margin:0;overflow-wrap:anywhere}.data-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.5rem;list-style:none;padding:0}.data-list li{background:var(--panel);border:1px solid var(--line);border-radius:.55rem;padding:.58rem .7rem}.count{color:var(--accent);font-weight:800}.controls{display:flex;gap:.7rem;flex-wrap:wrap;margin:1rem 0}input,textarea,select,button{font:inherit}input,textarea,select{width:100%;background:#09111e;color:var(--text);border:1px solid var(--line);border-radius:.55rem;padding:.7rem}textarea{min-height:95px;resize:vertical}label{font-weight:750;display:block;margin:.8rem 0 .25rem}.form-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:0 1rem}.full{grid-column:1/-1}button,.button{border:0;border-radius:.55rem;padding:.7rem 1rem;background:var(--accent);color:#062119;font-weight:850;cursor:pointer;text-decoration:none;display:inline-block}button.secondary{background:var(--panel2);color:var(--text);border:1px solid var(--line)}button.danger{background:#5c2c30;color:#fff}.saved{display:grid;gap:.7rem}.saved article{background:var(--panel);border:1px solid var(--line);border-radius:.7rem;padding:1rem}.saved time{color:var(--muted);font-size:.85rem}.empty{color:var(--muted)}footer{border-top:1px solid var(--line);padding:2rem 0;color:var(--muted);font-size:.9rem}.small{font-size:.9rem;color:var(--muted)}code{background:var(--panel2);padding:.12rem .3rem;border-radius:.3rem}@media(max-width:760px){.header-inner{align-items:flex-start;flex-direction:column;padding:.8rem 0}nav{padding-bottom:.3rem}.form-grid{grid-template-columns:1fr}.source dl{grid-template-columns:1fr}.source dd{margin-bottom:.4rem}main{padding-top:2rem}}
""".strip()

BUILDER_JS = r"""
(() => {
  const KEY = 'classic-notes-builds-v1';
  const form = document.querySelector('#build-form');
  const list = document.querySelector('#saved-builds');
  const status = document.querySelector('#save-status');
  const read = () => { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch { return []; } };
  const write = builds => localStorage.setItem(KEY, JSON.stringify(builds));
  const clean = value => String(value || '').trim();
  const render = () => {
    const builds = read();
    list.replaceChildren();
    if (!builds.length) {
      const p = document.createElement('p'); p.className = 'empty'; p.textContent = '아직 저장한 빌드가 없습니다.'; list.append(p); return;
    }
    builds.forEach(build => {
      const article = document.createElement('article');
      const title = document.createElement('h3'); title.textContent = build.name || '이름 없는 빌드';
      const meta = document.createElement('p'); meta.textContent = `챔피언: ${build.champion || '미지정'}`;
      const detail = document.createElement('p'); detail.textContent = `룬: ${build.runes || '-'} / 특성: ${build.masteries || '-'} / 아이템: ${build.items || '-'}`;
      const time = document.createElement('time'); time.dateTime = build.updatedAt; time.textContent = `저장: ${new Date(build.updatedAt).toLocaleString('ko-KR')}`;
      const remove = document.createElement('button'); remove.type = 'button'; remove.className = 'danger'; remove.textContent = '삭제'; remove.dataset.id = build.id;
      article.append(title, meta, detail, time, document.createElement('br'), remove); list.append(article);
    });
  };
  form.addEventListener('submit', event => {
    event.preventDefault();
    const data = new FormData(form);
    const build = { id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()), name: clean(data.get('name')), champion: clean(data.get('champion')), runes: clean(data.get('runes')), masteries: clean(data.get('masteries')), items: clean(data.get('items')), updatedAt: new Date().toISOString() };
    const builds = read(); builds.unshift(build); write(builds.slice(0, 30)); form.reset(); status.textContent = '이 브라우저에 저장했습니다.'; render();
  });
  list.addEventListener('click', event => {
    const id = event.target.dataset.id; if (!id) return;
    write(read().filter(build => build.id !== id)); status.textContent = '저장 항목을 삭제했습니다.'; render();
  });
  render();
})();
""".strip()



def href(path: str) -> str:
    return f"{BASE}{path}"


def canonical(path: str) -> str:
    return f"{SITE_URL}{path}"


def layout(path: str, title: str, description: str, body: str, kind: str = "WebPage", robots: str = "index,follow,max-image-preview:large") -> str:
    current = next((label for target, label in NAV if target == path), "")
    nav = "".join(
        f'<a href="{href(target)}"' + (' aria-current="page"' if label == current else "") + f'>{label}</a>'
        for target, label in NAV
    )
    structured = {
        "@context": "https://schema.org",
        "@type": kind,
        "name": title,
        "description": description,
        "url": canonical(path),
        "inLanguage": "ko-KR",
        "isPartOf": {"@type": "WebSite", "name": "클래식 노트", "url": f"{SITE_URL}/"},
    }
    json_ld = json.dumps(structured, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical(path)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="클래식 노트">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(description, quote=True)}">
<meta property="og:url" content="{canonical(path)}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{href('/assets/site.css')}">
<script type="application/ld+json">{json_ld}</script>
</head>
<body>
<a class="skip" href="#content">본문으로 이동</a>
<header class="site-header"><div class="wrap header-inner"><a class="brand" href="{href('/')}">클래식 <span>노트</span></a><nav aria-label="주요 메뉴">{nav}</nav></div></header>
<main id="content" class="wrap">{body}</main>
<footer><div class="wrap">비공식 정보성 팬 사이트 · Riot Games 또는 League of Legends의 공식 서비스가 아닙니다. · 데이터 확인일 {CHECKED_AT}</div></footer>
</body>
</html>
"""


def source_box(label: str, url: str) -> str:
    return f"""<aside class="source" aria-label="데이터 출처"><h2>출처와 검증 상태</h2><dl>
<dt>대상 데이터</dt><dd>{html.escape(label)}</dd>
<dt>검토 중인 출처</dt><dd><a href="{url}" rel="nofollow external">Riot Games Data Dragon {VERSION} 한국어 JSON</a></dd>
<dt>확인일</dt><dd><time datetime="{CHECKED_AT}">{CHECKED_AT}</time></dd>
<dt>공개 상태</dt><dd><strong>확인 중</strong> — 정책 검토가 끝날 때까지 게임 데이터와 에셋을 공개하지 않습니다.</dd>
</dl></aside>"""


def data_list(values: list[dict[str, str]]) -> str:
    if not values:
        return '<div class="notice"><strong>확인 중</strong> 정책·출처 검토 완료 전에는 항목명, 수치, 이미지 에셋을 공개하지 않습니다.</div>'
    return '<div class="notice"><strong>확인 중</strong> 검증된 항목이 아직 없습니다.</div>'


def write_page(path: str, content: str) -> None:
    destination = SITE / path.lstrip("/") / "index.html" if path != "/" else SITE / "index.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def main() -> None:
    # 보드의 Riot IP 출시 게이트에 따라 출처 URL만 기록하고 실제 게임 데이터·에셋은
    # 정책 검토가 끝날 때까지 배포 산출물에 넣지 않는다.
    datasets: dict[str, list[dict[str, str]]] = {key: [] for key in SOURCES}

    if SITE.exists():
        shutil.rmtree(SITE)
    (SITE / "assets").mkdir(parents=True)
    (SITE / "assets/site.css").write_text(CSS + "\n", encoding="utf-8")
    (SITE / "assets/builder.js").write_text(BUILDER_JS + "\n", encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")

    home_body = f"""<section class="hero"><p class="eyebrow">출처·정책 검증 우선</p><h1>기억 대신 출처로 준비하는<br>클래식 게임 정보 노트</h1><p class="lede">룬, 특성(마스터리), 아이템, 챔피언 레퍼런스의 공개 위치를 먼저 마련했습니다. 공식 정책과 현행 반영 여부가 검증될 때까지 게임 데이터·이미지는 공개하지 않습니다.</p><div class="notice"><strong>정확성 안내</strong> Data Dragon {VERSION} 출처 후보는 확인했지만, 시즌3 또는 2026 롤 클래식과의 일치 및 공개 이용 조건은 <b>확인 중</b>입니다.</div></section>
<section><h2>주제별 빠른 탐색</h2><div class="grid">
<a class="card" href="{href('/runes/')}"><span class="tag">룬</span><h3>룬 레퍼런스</h3><p>출처 후보와 공개 검토 상태</p></a>
<a class="card" href="{href('/masteries/')}"><span class="tag">특성</span><h3>특성(마스터리)</h3><p>출처 후보와 공개 검토 상태</p></a>
<a class="card" href="{href('/season3-items/')}"><span class="tag">아이템</span><h3>아이템 레퍼런스</h3><p>출처 후보와 공개 검토 상태</p></a>
<a class="card" href="{href('/champions/')}"><span class="tag">챔피언</span><h3>챔피언 레퍼런스</h3><p>출처 후보와 공개 검토 상태</p></a>
<a class="card" href="{href('/builder/')}"><span class="tag">재방문 도구</span><h3>빌드 메모 저장</h3><p>계정 없이 이 브라우저에 빌드를 저장</p></a>
</div></section>
<section><h2>편집 원칙</h2><div class="grid"><div class="card"><h3>출처 우선</h3><p>출처와 공개 조건이 함께 확인된 항목만 향후 노출합니다.</p></div><div class="card"><h3>현행성 구분</h3><p>검증되지 않은 신규 모드 수치에는 추측 대신 ‘확인 중’을 표시합니다.</p></div><div class="card"><h3>중립 셸 우선</h3><p>정책 검토 중에는 로고·원화·게임 UI·게임 데이터 없이 페이지와 개인 메모 도구만 제공합니다.</p></div></div></section>"""
    write_page("/", layout("/", "롤 클래식 정보 허브 | 룬·특성·시즌3 아이템·챔피언", "롤 클래식 룬, 특성(마스터리), 시즌3 아이템, 챔피언을 공식 역사 데이터 출처와 함께 확인하세요.", home_body, "WebSite"))

    refs = [
        ("/runes/", "롤클래식 룬 레퍼런스 | 공개 검증 중", "롤클래식 룬 레퍼런스의 출처 후보, 확인일, 공개 검토 상태를 안내합니다.", "롤 클래식 룬", "runes", "룬"),
        ("/masteries/", "롤클래식 특성·마스터리 | 공개 검증 중", "롤클래식 특성(마스터리) 레퍼런스의 출처 후보와 공개 검토 상태를 안내합니다.", "롤 클래식 특성(마스터리)", "masteries", "특성"),
        ("/season3-items/", "시즌3 아이템 레퍼런스 | 공개 검증 중", "시즌3 아이템 레퍼런스의 Data Dragon 출처 후보와 확인일을 안내합니다.", "시즌3 아이템", "items", "아이템"),
        ("/champions/", "롤클래식 챔피언 레퍼런스 | 공개 검증 중", "롤클래식 챔피언 레퍼런스의 출처 후보와 현행 반영 검토 상태를 안내합니다.", "롤 클래식 챔피언", "champions", "챔피언"),
    ]
    for path, title, description, heading, key, noun in refs:
        values = datasets[key]
        body = f"""<section class="hero"><p class="eyebrow">공개 전 검증</p><h1>{heading}</h1><p class="lede">Data Dragon {VERSION} 한국어 JSON을 출처 후보로 확인했습니다. 정책 및 2026 현행 구성 검토가 끝날 때까지 실제 {noun} 항목은 공개하지 않습니다.</p></section>{source_box(heading + ' 레퍼런스', SOURCES[key])}<section><h2>{noun} 데이터 상태</h2>{data_list(values)}</section>"""
        write_page(path, layout(path, title, description, body, "CollectionPage"))

    builder_body = f"""<section class="hero"><p class="eyebrow">클라이언트 전용 도구</p><h1>클래식 빌드 메모</h1><p class="lede">계정 없이 이 브라우저에 룬·특성·아이템 메모를 저장하세요. 입력 내용은 서버로 전송되지 않습니다.</p></section>
<section><h2>새 빌드 저장</h2><form id="build-form" class="form-grid"><div><label for="name">빌드 이름</label><input id="name" name="name" required maxlength="80" placeholder="예: 탑 연습 빌드"></div><div><label for="champion">캐릭터 메모</label><input id="champion" name="champion" maxlength="80" placeholder="직접 입력"></div><div class="full"><label for="runes">룬 메모</label><textarea id="runes" name="runes" maxlength="500" placeholder="현재 모드 적용 여부를 직접 확인한 뒤 기록하세요."></textarea></div><div class="full"><label for="masteries">특성(마스터리) 메모</label><textarea id="masteries" name="masteries" maxlength="500"></textarea></div><div class="full"><label for="items">아이템 메모</label><textarea id="items" name="items" maxlength="500"></textarea></div><div class="full controls"><button type="submit">이 브라우저에 저장</button><span id="save-status" role="status" aria-live="polite"></span></div></form></section>
<section><h2>저장한 빌드</h2><div id="saved-builds" class="saved"></div><p class="small">브라우저 데이터 삭제 시 저장 내용도 사라집니다. 최대 30개를 보관합니다.</p></section><script src="{href('/assets/builder.js')}" defer></script>"""
    write_page("/builder/", layout("/builder/", "롤 클래식 빌드 저장 도구 | 브라우저 전용", "롤 클래식 룬, 특성, 아이템 빌드 메모를 계정 없이 브라우저에 저장하는 클라이언트 전용 도구입니다.", builder_body, "SoftwareApplication"))

    not_found = f"""<section class="hero"><p class="eyebrow">404</p><h1>페이지를 찾을 수 없습니다</h1><p class="lede">주소가 바뀌었거나 아직 준비되지 않은 페이지입니다.</p><p><a class="button" href="{href('/')}">홈으로 돌아가기</a></p></section>"""
    (SITE / "404.html").write_text(layout("/404.html", "페이지를 찾을 수 없습니다 | 클래식 노트", "요청한 페이지를 찾을 수 없습니다.", not_found, robots="noindex,follow"), encoding="utf-8")

    urls = [path for path, _ in NAV]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{canonical(path)}</loc><lastmod>{CHECKED_AT}</lastmod></url>\n" for path in urls) + "</urlset>\n"
    (SITE / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")

    manifest = {"generatedAt": date.today().isoformat(), "sourceVersion": VERSION, "checkedAt": CHECKED_AT, "counts": {key: len(value) for key, value in datasets.items()}, "sources": SOURCES}
    (SITE / "data-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
