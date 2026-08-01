# Riot IP 공개 배포 게이트

확인일: 2026-08-02

## 현재 판정

상위 AIW-166 이슈의 2026-08-02 보드 코멘트는 Riot 공식 Legal Jibber Jabber와 Developer 정책을 근거로, Riot IP·Data Dragon 에셋을 포함한 공개 배포 및 광고 신청을 정책 판단 전까지 중단하도록 지시했다. 동시에 색인 시간을 확보하기 위해 정책상 안전한 중립 정적 셸은 먼저 배포하도록 했다.

따라서 이번 MVP는 다음만 공개한다.

- 중립 브랜드 `클래식 노트`
- 홈과 룬·특성·아이템·챔피언 레퍼런스 URL
- 출처 후보 URL, 확인일, `확인 중` 상태
- 사용자가 직접 입력하는 브라우저 전용 빌드 메모
- robots, sitemap, canonical, Open Graph, JSON-LD, 404

다음은 공개하지 않는다.

- Data Dragon에서 추출한 챔피언·아이템·룬·마스터리 이름과 수치
- Data Dragon 이미지 에셋
- Riot 로고, 챔피언 원화, 공식 게임 UI
- 광고 또는 수익화 코드

## 공식 원문

- Riot Games Legal Jibber Jabber: https://www.riotgames.com/en/legal
- Riot Developer General Policies: https://developer.riotgames.com/policies/general
- Riot Developer Data Dragon 문서: https://developer.riotgames.com/docs/lol#data-dragon
- Data Dragon 버전 목록: https://ddragon.leagueoflegends.com/api/versions.json

## 해제 조건

보드가 운영 주체의 법적 지위와 허용 경로를 결정하고, 필요한 Riot 서면 허가 또는 Developer Portal 등록·승인 상태를 확인한 뒤 명시적으로 게임 데이터/에셋 공개를 허용해야 한다. 해제 전에는 `scripts/build.py`의 빈 데이터셋 게이트를 제거하지 않는다.

이 문서는 법률 자문이 아니라 공식 정책 원문과 보드 지시에 따른 출시 위험 통제 기록이다.
