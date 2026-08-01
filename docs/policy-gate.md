# Riot IP 공개 배포 게이트

확인일: 2026-08-02

## 현재 판정

`public_distribution=true`로 전환한다.

사용자가 `ai-worker-lab`을 등록 사업체·법인이 아닌 개인 비상업 프로젝트 관리용 GitHub Organization으로 확인했다. 해당 Hub는 광고·결제·후원·유료 기능이 없는 개인 무료 팬 프로젝트다. 따라서 `Legal Jibber Jabber`의 “business or legal entity” 차단 전제는 이 프로젝트에 적용되지 않는다.

Riot 공식 정책에서 이 사실관계의 Data Dragon 공개를 직접 금지하는 조항은 확인되지 않았다. 오히려 다음 조건부 허용 근거가 있다.

- `Legal Jibber Jabber`: 규칙 준수를 조건으로 비상업 커뮤니티 사용에 대한 개인적·제한적 라이선스를 부여하고, 팬 프로젝트 공유 시 지정 고지를 요구한다.
- Riot Developer `General Policies`: 제품 개발·마케팅에 사용할 수 있는 자산으로 Data Dragon을 열거하고, 눈에 띄는 비공식 제품 고지를 요구한다.
- League of Legends 개발자 문서: Data Dragon이 정적 데이터 파일과 게임 에셋을 제공한다고 명시한다.

Developer Portal 제품 등록·감사는 명시적 정책 의무이므로 공개와 병행해 후속 운영 작업으로 추적한다. 등록 계획을 완료로 표현하지 않는다.

## 운영 주체·수익화

- 운영 주체: 개인 비상업 프로젝트
- GitHub Organization: 개인 프로젝트 정리·운영 용도, 등록 사업체·법인 아님
- 광고·결제·후원·유료 기능: 없음
- 현재 수익화 계획: 없음

## 공개 단일 데이터셋

- 버전/로케일: `3.13.24/ko_KR`
- 이유: `3.13.24`는 시즌 3 말기 기준선이다. `3.15.5`는 Yasuo, 장신구, 프리시즌 지원 아이템과 교체된 특성 체계를 포함해 시즌 3 역사 기준으로 부적합하다.
- 한계: 2026 League Classic은 단일 역사 패치의 완전 복제가 아니므로 현행 목록·수치와 동일하다고 주장하지 않는다.
- 제외: 공식 아카이브가 제공하지 않는 마스터리 트리 배경·연결선

## 필수 조건

- Riot Developer General Policies의 비공식 제품 고지를 눈에 띄게 표시
- `Legal Jibber Jabber`의 팬 프로젝트/에셋 소유 고지를 눈에 띄게 표시
- Data Dragon 출처·버전·로케일·확인일·현행성 한계 표시
- Riot 로고·공식 서비스로 혼동될 브랜딩 제외
- 제품명·메타 제목은 일반 명칭 `클래식 노트` 사용. GitHub Pages 등록 도메인은 `ai-worker-lab.github.io`이며 기존 저장소 경로에 직접 금지 조항이 적용된다고 단정할 근거는 확인되지 않았다. Portal 감사에서 변경 요청 시 일반 slug로 이전
- 광고·결제·후원·유료 기능 제외
- Developer Portal 제품 등록·감사 후속 추적

## 공식 원문

- Riot Games `Legal Jibber Jabber` (Last Updated: August 2018): https://www.riotgames.com/en/legal
- Riot Developer `General Policies` (LAST UPDATED: MARCH 11, 2025): https://developer.riotgames.com/policies/general
- Riot Developer `League of Legends` — Data Dragon: https://developer.riotgames.com/docs/lol#data-dragon
- Riot Games `League of Legends Classic`: https://www.leagueoflegends.com/en-us/classic/
- Data Dragon 공식 버전 목록: https://ddragon.leagueoflegends.com/api/versions.json

이 문서는 법률 자문이 아니라 Riot 공식 정책에 대한 출시 전 운영 검토다. Riot은 정책에 따라 허용을 철회할 수 있으므로 등록·감사 결과와 정책 변경을 계속 확인한다.
