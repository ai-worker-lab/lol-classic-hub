# AIW-185 실행 작업

## Phase 1 — Setup

- [x] T001 [AIW-185] 기존 빌드·검증·배포 구조와 Data Dragon 관계 수치를 확인한다.
- [x] T002 [AIW-185] 기능 명세와 구현 계획을 작성한다.

Checkpoint: spec → plan 완료.

## Phase 2 — Foundational

- [x] T003 [AIW-185] 테스트에서 요구하는 아이템 ID 보존·형제 수량 집계 API를 정의하고 RED를 확인한다.
- [x] T004 [AIW-185] 누락·순환·최대 깊이 방어 렌더링 테스트를 RED→GREEN으로 구현한다.

Checkpoint: 관계 엔진 단위 테스트 통과.

## Phase 3 — User Story P1

- [x] T005 [AIW-185] 205개 상세 URL과 하위·현재·상위 트리 HTML을 생성한다.
- [x] T006 [AIW-185] 목록 카드 링크와 이름·ID 검색을 추가한다.
- [x] T007 [AIW-185] 사이트맵과 내부 링크 검증을 상세 URL까지 확장한다.

Checkpoint: 직접 URL·목록 진입·노드 이동·뒤로 가기 경로 검증.

## Phase 4 — User Story P2/P3

- [x] T008 [AIW-185] 노드 가격·조합 비용·구매 가능 여부·맵 제한 배지를 구현한다.
- [x] T009 [AIW-185] 중복 수량 `×N`과 관계 없음 상태를 회귀 검증한다.
- [x] T010 [AIW-185] 데스크톱 3단·모바일 세로 구조와 포커스 스타일을 구현한다.

Checkpoint: 대표 기본·중간·최종·분기·중복 아이템 검증.

## Phase 5 — Verification & Delivery

- [x] T011 [AIW-185] 정적 빌드와 전체 검증을 실행한다.
- [x] T012 [AIW-185] 독립 코드 리뷰를 받고 발견 사항을 수정한다.
- [x] T013 [AIW-185] 의도된 변경만 커밋·main 반영하고 GitHub Pages 성공을 확인한다.
- [x] T014 [AIW-185] 공개 URL에서 목록과 대표 상세 트리를 검증하고 SHA·URL을 보고한다.

Checkpoint: 자동 배포와 실공개 검증 완료.
