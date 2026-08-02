# AIW-185 구현 계획 — 아이템 조합·업그레이드 트리

## Summary

기존 Python 정적 빌드에 아이템 ID 보존, 재귀 관계 렌더러, 205개 상세 페이지, 목록 검색, 반응형·접근성 스타일을 추가한다. 관계는 공식 `item.json`만 사용하며 빌드 검증에서 수치·중복·링크·방어 동작을 고정한다.

## Technical Context

- Runtime: Python 3 표준 라이브러리
- Output: GitHub Pages용 `site/` 정적 HTML/CSS/JS
- Data: `assets/upstream/3.13.24/data/ko_KR/item.json`
- Tests: `unittest` 단위 회귀 + `scripts/verify.py` 산출물 계약 검증
- Deploy: `.github/workflows/pages.yml`, `main` push

## Constitution Check

- Spec-first: `docs/aiw-185-spec.md` 작성 후 계획·작업·구현 순서 유지.
- SSoT: 수작업 관계표 없이 Data Dragon `from`·`into` 직접 사용.
- 안전성: 누락·순환·깊이 제한 방어, HTML 이스케이프, 외부 입력 없음.
- 접근성: 링크 기반 노드, 키보드 포커스, 제목·단계 라벨, 모바일 세로 순서.
- 운영 경계: 기존 Riot 고지·출처·버전·비수익화 정책 유지.

## Project Structure

- `scripts/build.py`: 데이터 로드, 관계 렌더링, 상세 페이지·검색 자산 생성.
- `scripts/verify.py`: 상세 페이지·관계 수치·중복·사이트맵·링크 계약 검증.
- `tests/test_item_trees.py`: 집계·누락·순환·깊이 제한 단위 회귀.
- `site/season3-items/{id}/index.html`: 생성 산출물 205개.
- `docs/aiw-185-{spec,plan,tasks}.md`: SDD 추적 산출물.

## Design

1. 사이트 삭제·쓰기 전에 공식 JSON SHA-256을 검증하고 아이템 ID를 숫자로 제한한 뒤 `_id`로 보존한다.
2. 형제 참조는 `Counter`로 집계하고 최초 등장 순서를 유지한다.
3. 재귀 렌더러는 방향별 `visited` 불변 집합과 `depth/max_depth`를 전달한다.
4. 상세 페이지는 하위·현재·상위 3개 `section`을 DOM 순서대로 생성한다.
5. 목록 카드 전체를 상세 링크로 만들고 이름·ID 검색을 점진적으로 추가한다.
6. 출력 경로가 `site/` 하위인지 확인하고 사이트맵 및 검증 대상에 205개 상세 URL을 추가한다.

## Verification

- RED: 새 단위 테스트가 구현 전 import/동작 실패함을 확인.
- GREEN: `python3 -m unittest tests.test_item_trees -v`.
- Build: `python3 scripts/build.py`.
- Contract: `python3 scripts/verify.py`.
- Review: 독립 diff 리뷰 후 결함 수정.
- Deploy: main 반영 뒤 Pages 성공 및 공개 목록·대표 상세 URL HTTP 200 확인.

## Complexity Tracking

재귀 트리는 현재 데이터의 순환이 없지만 향후 변경을 대비해 최대 깊이 8과 경로별 방문 집합을 유지한다. 205개 규모에서 정적 중복 HTML은 허용하며 런타임 서버·클라이언트 데이터 의존성을 추가하지 않는다.
