# 클래식 노트 — 시즌 3 데이터 기록관

Riot Games Data Dragon `3.13.24/ko_KR`의 시즌 3 챔피언·아이템·룬·특성 역사 데이터와 공식 아이콘을 제공하는 개인 비상업 한국어 팬 프로젝트입니다.

공개 URL: https://ai-worker-lab.github.io/lol-classic-hub/

> 이 사이트는 Riot Games 또는 League of Legends의 공식 서비스가 아닙니다. Data Dragon 자료는 시즌 3 역사 스냅샷이며 2026 League Classic의 현행 목록·수치와 동일함을 보증하지 않습니다. 광고·결제·후원·유료 기능이 없습니다.

## 제공 페이지

- `/` — 홈과 데이터 범위·정확성 안내
- `/runes/` — 룬 296개
- `/masteries/` — 특성(마스터리) 56개
- `/season3-items/` — 아이템 205개 목록·이름/ID 검색
- `/season3-items/{id}/` — 아이템별 하위 재료·현재 아이템·상위 업그레이드 트리
- `/champions/` — 챔피언 116개
- `/builder/` — 계정 없는 브라우저 전용 빌드 메모
- `/robots.txt`, `/sitemap.xml`, `/404.html`

공개 페이지는 데이터 레코드 673개와 공식 이미지 참조 673개를 포함합니다. 중복을 제거한 공식 이미지 파일은 447개입니다. 공식 아카이브가 제공하지 않는 마스터리 트리 배경·연결선은 포함하지 않습니다.

## 단일 데이터셋 결정

공개 데이터 기준은 `3.13.24/ko_KR` 하나입니다.

- `3.13.24`: 챔피언 116, 아이템 205, 룬 296, 특성 56
- `3.15.5`: Yasuo, 장신구, 프리시즌 지원 아이템, 교체된 특성 체계를 포함

따라서 프리시즌 변경 전 시즌 3 역사 기준선으로 `3.13.24`를 채택했고, 한국어 사이트 표시에는 같은 버전의 `ko_KR` JSON을 사용합니다. 2026 League Classic은 단일 역사 패치의 완전 복제가 아니므로 이 데이터는 역사 참고 자료로만 제공합니다.

## 공식 출처

- 버전 목록: https://ddragon.leagueoflegends.com/api/versions.json
- 챔피언: https://ddragon.leagueoflegends.com/cdn/3.13.24/data/ko_KR/champion.json
- 아이템: https://ddragon.leagueoflegends.com/cdn/3.13.24/data/ko_KR/item.json
- 특성: https://ddragon.leagueoflegends.com/cdn/3.13.24/data/ko_KR/mastery.json
- 룬: https://ddragon.leagueoflegends.com/cdn/3.13.24/data/ko_KR/rune.json
- Riot Legal Jibber Jabber: https://www.riotgames.com/en/legal
- Riot Developer General Policies: https://developer.riotgames.com/policies/general
- Riot Data Dragon 문서: https://developer.riotgames.com/docs/lol#data-dragon

확인일: 2026-08-02

## 로컬 실행

Python 3만 필요합니다. 빌드는 저장소에 검증·고정한 공식 JSON과 이미지 파일을 사용하며 실행 중 외부 네트워크를 요구하지 않습니다.

```bash
python3 scripts/build.py
python3 scripts/verify.py
python3 scripts/serve.py
```

브라우저에서 http://127.0.0.1:8000/lol-classic-hub/ 을 엽니다.

검증 스크립트는 다음을 확인합니다.

- 데이터 개수 `116/205/56/296`
- 이미지 참조 673개, 고유 파일 447개, 누락 0
- 데이터 SHA-256
- 두 필수 Riot 고지와 Data Dragon 버전·로케일·확인일·현행성 한계
- Riot 로고·비공식 이미지 경로·대표 수익화 코드 부재
- 아이템 상세 205개, `from`/`into` 관계 279/267개, 중복 수량, 누락·순환·깨진 링크 0
- canonical, description, Open Graph, JSON-LD, robots, sitemap, 내부 링크

## 배포

GitHub Pages를 사용합니다. `main` push가 `.github/workflows/pages.yml`을 실행합니다.

```bash
git push origin main
gh run list --workflow pages.yml --limit 1
curl -I https://ai-worker-lab.github.io/lol-classic-hub/
```

워크플로는 저장소의 고정 데이터·에셋으로 사이트를 다시 생성하고 검증한 뒤 `site/`를 배포합니다.

## 정책·운영 경계

- 운영 주체: 등록 사업체·법인이 아닌 개인 비상업 프로젝트
- Riot 로고 및 공식 서비스로 혼동될 브랜딩 금지
- 광고·결제·후원·유료 기능 금지
- 공식 출처 없는 자산 대체 금지
- Developer Portal 제품 등록·감사는 별도 운영 작업으로 병행
- Riot 정책 변경이나 감사 결과는 `docs/policy-gate.md`에 반영

이 정책 검토는 법률 자문이 아닙니다.

## 개발 문서

- `docs/spec.md` — 제품 요구사항과 성공 기준
- `docs/plan.md` — 구현·검증·배포 계획
- `docs/tasks.md` — 실행 작업 목록
- `docs/policy-gate.md` — 운영 주체와 Riot 정책 판정
- `docs/sources-and-policy.md` — 공식 출처·브랜딩·데이터 인용 규칙
- `docs/aiw-183-release-assessment.md` — 공개 재검증 상세 보고
- `docs/aiw-185-{spec,plan,tasks}.md` — 아이템 조합·업그레이드 트리 SDD 산출물
