# 클래식 노트 — 롤 클래식 정보 허브

롤 클래식 관련 한국어 검색 의도에 대응할 공개 URL과 출처 검토 상태를 먼저 제공하는 정적 정보 허브입니다. Riot 공식 Data Dragon `3.15.5` 한국어 역사 스냅샷은 출처 후보로 확인했지만, Riot IP 공개 이용 정책과 2026 현행 반영 여부가 검토 중이므로 MVP에는 항목명·수치·이미지 에셋을 노출하지 않습니다.

공개 URL: https://ai-worker-lab.github.io/lol-classic-hub/

> 비공식 정보성 사이트이며 Riot Games 또는 League of Legends의 공식 서비스가 아닙니다. 정책 검토 중에는 Data Dragon 항목명·수치·이미지, 공식 로고·챔피언 원화·게임 UI를 사용하지 않습니다.

## 제공 페이지

- `/` — 롤 클래식 허브 홈
- `/runes/` — 롤클래식 룬 역사 목록
- `/masteries/` — 롤클래식 특성(마스터리) 역사 목록
- `/season3-items/` — 시즌3 아이템 역사 목록
- `/champions/` — 롤클래식 챔피언 역사 목록
- `/builder/` — 계정 없는 브라우저 전용 빌드 메모 저장 도구
- `/robots.txt`, `/sitemap.xml`, `/404.html`

## 로컬 실행

Python 3만 필요합니다. 정책 게이트가 활성화된 현재 생성기는 외부 데이터를 내려받지 않습니다.

```bash
python3 scripts/build.py
python3 scripts/verify.py
python3 scripts/serve.py
```

브라우저에서 http://127.0.0.1:8000/lol-classic-hub/ 을 엽니다. `serve.py`는 GitHub Pages의 프로젝트 경로(`/lol-classic-hub/`)를 로컬에서도 동일하게 재현합니다.

## 배포

월 고정비 0인 GitHub Pages를 사용합니다.

1. GitHub 저장소 Settings → Pages의 Source를 **GitHub Actions**로 설정합니다.
2. `AIW-168-48-mvp` 브랜치에 push하면 `.github/workflows/pages.yml`이 실행됩니다.
3. workflow는 게임 데이터가 비어 있는 정책 안전 셸을 다시 생성하고 정적 검증을 통과한 뒤 `site/`를 배포합니다.
4. Actions 성공 후 공개 URL과 `robots.txt`, `sitemap.xml`, 핵심 URL을 `curl`로 확인합니다.

```bash
git push -u origin AIW-168-48-mvp
gh run list --workflow pages.yml --limit 1
curl -I https://ai-worker-lab.github.io/lol-classic-hub/
```

## 데이터 갱신 — 정책 게이트 해제 후에만

데이터 SSoT는 `scripts/build.py`의 `VERSION`, `CHECKED_AT`, `SOURCES`입니다.

1. 먼저 `docs/policy-gate.md`의 해제 조건을 충족하고 보드의 명시적 공개 승인을 기록합니다.
2. Riot Data Dragon 공식 CDN에서 목표 버전과 한국어 JSON의 HTTP 200을 확인합니다.
3. `VERSION`과 실제 확인일인 `CHECKED_AT`을 갱신합니다.
4. 별도 변경에서 데이터 파서를 추가하고 `python3 scripts/build.py && python3 scripts/verify.py`를 실행합니다.
5. 생성된 `site/` diff에서 추가·삭제 항목, 수치, 에셋, 출처 URL을 검토합니다.
6. 신규 롤 클래식 현행 적용 근거가 없으면 `확인 중` 문구를 제거하지 않습니다.
7. 검증된 근거를 URL·확인일과 함께 기록합니다.

정책 해제 후 검토할 출처 후보(현재 페이지에는 데이터·아이콘 미노출):

- https://ddragon.leagueoflegends.com/cdn/3.15.5/data/ko_KR/champion.json
- https://ddragon.leagueoflegends.com/cdn/3.15.5/data/ko_KR/item.json
- https://ddragon.leagueoflegends.com/cdn/3.15.5/data/ko_KR/mastery.json
- https://ddragon.leagueoflegends.com/cdn/3.15.5/data/ko_KR/rune.json

확인일: 2026-08-02

## 운영 기준

### D+14 — 첫 배포일 기준

- Search Console 또는 호스팅에서 실측 가능한 페이지뷰, 유입 질의, 색인 수, 체류 지표를 기록합니다.
- 광고 승인 준비 여부를 확인하되, 검증되지 않은 추정 트래픽이나 수익을 기록하지 않습니다.
- `robots.txt`, `sitemap.xml`, canonical 상태와 404를 다시 점검합니다.
- Riot 정책 리서치 결과를 반영하고 브랜드·이미지·수익화 위험을 재검토합니다.

### D+30 — 보드 판단

- 실측 트래픽으로 월 환산 페이지뷰를 계산합니다.
- 월 환산 페이지뷰가 10,000 미만이면 신규 기능 확장을 중단하고 정적 자산과 색인만 보존합니다.
- 10,000 이상이면 유입 질의별 콘텐츠 정확성, 재방문율, 광고 승인 상태를 근거로 다음 투자 여부를 보드가 결정합니다.

## 범위 밖

계정, 게시판, 댓글, 신고, 서버 DB, 유료 API, 유료 인프라는 MVP 범위에 없습니다.

## 개발 문서

- `docs/spec.md` — 요구사항과 성공 기준
- `docs/plan.md` — 구현·검증 계획
- `docs/tasks.md` — 추적 가능한 작업 목록
- `docs/policy-gate.md` — Riot IP 공개 배포 게이트와 해제 조건
