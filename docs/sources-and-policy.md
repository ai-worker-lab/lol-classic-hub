# Riot 정책·시즌 3 데이터 출처

확인일: 2026-08-02 (KST)

> 이 문서는 법률 자문이 아니다. Riot Games의 현재 공식 정책과 공식 데이터 엔드포인트를 바탕으로 한 출시 전 운영 검토다. Riot은 허용을 철회하거나 정책을 변경할 수 있으므로 공개 전과 수익화 전 다시 확인한다.

## 구현자용 즉시 요약

### 지금 사용 가능한 공식 URL

- 정책: https://www.riotgames.com/en/legal
- 개발자 공통 정책: https://developer.riotgames.com/policies/general
- League of Legends / Data Dragon 문서: https://developer.riotgames.com/docs/lol#data-dragon
- Data Dragon 버전 목록: https://ddragon.leagueoflegends.com/api/versions.json
- `3.13.24/ko_KR` 챔피언: https://ddragon.leagueoflegends.com/cdn/3.13.24/data/ko_KR/champion.json
- `3.13.24/ko_KR` 아이템: https://ddragon.leagueoflegends.com/cdn/3.13.24/data/ko_KR/item.json
- `3.13.24/ko_KR` 룬: https://ddragon.leagueoflegends.com/cdn/3.13.24/data/ko_KR/rune.json
- `3.13.24/ko_KR` 특성(마스터리): https://ddragon.leagueoflegends.com/cdn/3.13.24/data/ko_KR/mastery.json
- 현재 League of Legends Classic 공식 페이지: https://www.leagueoflegends.com/en-us/classic/

### 구현 규칙

1. 수치·설명·이미지 파일명은 위 `3.13.24/ko_KR` 데이터에서만 가져온다. 모델 기억, 검색 스니펫, 위키, 임의 CDN으로 빈칸을 채우지 않는다.
2. 화면에는 반드시 `Riot Data Dragon 3.13.24 / ko_KR 역사 스냅샷`이라고 표시한다. 현재 League of Legends Classic과 같다고 쓰지 않는다.
3. 공식 데이터에 없거나 상충하는 값은 `확인 중`으로 표시하고 공개 목록에서 제외한다. 현대 데이터나 다른 패치 값으로 대체하지 않는다.
4. Riot·League of Legends 로고, 공식 사이트와 혼동되는 UI, Press Kit 밖의 이미지, 제3자 위키 이미지는 사용하지 않는다.
5. 공개 제품명·도메인·소셜 계정·검색 태그에는 `Riot`, `League of Legends`, `LoL`, `롤`, 챔피언명 등 Riot 표장을 넣지 않는다. 현재 저장소명 `lol-classic-hub`도 공개 식별자로는 안전 판정하지 않는다.
6. 광고·결제·후원·구독·유료 기능은 넣지 않는다. 수익화는 Developer Portal 등록과 `Approved` 또는 `Acknowledged` 상태를 확인한 뒤 별도 정책 검토를 거친다.
7. 공개 전에 Developer Portal 제품 등록·감사를 진행하고, 아래 두 고지를 사용자가 쉽게 볼 수 있는 위치에 표시한다.

## 1. 확인된 운영 사실과 판정 범위

프로젝트 소유자가 `ai-worker-lab` GitHub Organization은 개인 비상업 프로젝트를 정리하기 위한 곳이며 사업체나 법인이 아니라고 확인했다. 현재 프로젝트는 무료 정적 정보 사이트이고 광고·결제·후원·유료 기능을 사용하지 않는다.

이는 운영자가 제공한 사실관계이지 법인등기나 사업자 상태에 대한 독립 법률 확인은 아니다. 운영 주체나 수익화가 바뀌면 이 문서의 판정은 즉시 만료된다.

현재 사실관계에서는 `Legal Jibber Jabber`의 비상업 커뮤니티용 개인 라이선스 경로를 검토할 수 있고, Riot Developer `General Policies`가 Data Dragon을 제품 개발·마케팅에 사용할 수 있는 자산으로 명시하므로 **정책 조건을 지킨 Data Dragon 기반 역사 정보 페이지는 진행 가능**하다고 판단한다. 다만 Developer Portal 등록·감사는 별도 명시 의무이므로 공개 운영과 함께 완료해야 하며, 등록 계획을 완료 사실처럼 표현하면 안 된다.

## 2. 공식 정책 근거

### 2.1 Riot Games, `Legal Jibber Jabber`

- 발행자: Riot Games
- 표시 버전: `Last Updated: August 2018`
- URL: https://www.riotgames.com/en/legal
- 신뢰도: 높음 — Riot 공식 법률 페이지

확인된 사실:

- 모든 규칙 준수를 조건으로 Riot IP를 비상업 커뮤니티 용도로 사용·표시하고 파생물을 만들 수 있는 개인적·비독점적·재허가 불가·양도 불가·철회 가능한 제한 라이선스를 제시한다.
- 서면 라이선스 없이 사업체나 법인이 관여하는 프로젝트, 크라우드펀딩, 페이월 등 상업 프로젝트를 금지한다. 일부 광고·스트리밍·API 정책 예외가 있으나 자동 허용이 아니다.
- 서면 라이선스 없이 Riot 로고·상표를 프로젝트, 웹사이트, 광고 등에 사용할 수 없고, Riot 표장·상품명·캐릭터명 등을 사용한 도메인·소셜 계정·유사 식별자 및 인터넷 검색 태그 등록을 금지한다.
- 팬 프로젝트 공유 시 다음 고지를 눈에 띄게 표시하도록 요구한다.

> [The title of your Project] was created under Riot Games' "Legal Jibber Jabber" policy using assets owned by Riot Games. Riot Games does not endorse or sponsor this project.

제품 적용 해석:

- 개인·무료·비상업 운영이라는 현재 사실관계는 비상업 커뮤니티 경로와 부합한다.
- `lol-classic-hub`는 `LoL`을 공개 식별자에 포함하므로, 이 문서만으로 공개 제품명·도메인·저장소명으로 안전하다고 결론 내릴 수 없다. 가장 작은 안전 조치는 사용자 노출 제품명을 `2013 MOBA 데이터 기록관` 같은 일반 명칭으로 바꾸고 공개 URL·소셜 계정·메타 키워드에서도 Riot 표장을 제외하는 것이다.
- 데이터 본문에서 출처와 대상을 사실적으로 식별하는 범위를 넘어 Riot 표장을 브랜드처럼 강조하지 않는다.

### 2.2 Riot Developer, `General Policies`

- 발행자: Riot Games Developer Relations
- 표시 버전: `LAST UPDATED: MARCH 11, 2025`
- URL: https://developer.riotgames.com/policies/general
- 신뢰도: 높음 — Riot 공식 개발자 정책

확인된 사실:

- 제품 개발·마케팅에 사용할 수 있는 자산으로 `Data Dragon`을 명시한다.
- 모든 제품은 Developer Portal에 등록되고 Riot의 감사를 받아야 하며, 기능 변경도 제품 페이지를 통해 감사받아야 한다고 명시한다.
- 수익화 제품은 Developer Portal에 등록되어 있고 상태가 `Approved` 또는 `Acknowledged`여야 한다. 무료 접근 계층, 변형적 가치 등 추가 조건도 둔다.
- 다음 비공식 제품 고지를 사용자가 쉽게 볼 수 있는 위치에 표시하도록 요구한다.

> [Your product] isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

제품 적용 해석:

- Data Dragon의 데이터 파일과 연결 에셋은 출처 불명 이미지보다 우선하는 허용 경로다.
- 현재 수익화는 0으로 유지한다. `Legal Jibber Jabber`의 개인 광고 예외만 보고 광고를 켜지 않으며, 최신 Developer 정책의 등록·제품 상태 조건을 먼저 충족한다.
- API를 호출하지 않는 정적 사이트라도 “모든 제품” 등록 문구와 League 개발자 문서의 “플레이어를 위한 제품은 공식 API 사용 여부와 무관하게 등록” 문구를 보수적으로 적용한다.

### 2.3 Riot Developer, `League of Legends` — Data Dragon

- 발행자: Riot Games Developer Relations
- URL: https://developer.riotgames.com/docs/lol#data-dragon
- 신뢰도: 높음 — Riot 공식 개발자 문서

확인된 사실:

- Data Dragon은 챔피언, 아이템, 룬 등을 포함한 League of Legends 게임 데이터와 에셋을 중앙 제공하며 제3자 개발자가 사용할 수 있다고 설명한다.
- 정적 데이터는 데이터 파일과 게임 에셋의 두 종류이고, URL에는 버전과 언어 코드가 포함된다.
- 패치별 Data Dragon 갱신은 수동이어서 실제 패치 직후 즉시 갱신되지 않을 수 있다.
- Data Dragon 버전은 지역 클라이언트 버전과 항상 같지 않다.
- 한 패치에 빌드가 여러 개면 오류 수정일 수 있으므로 해당 패치의 가장 최근 Data Dragon 빌드를 사용하라고 안내한다.

제품 적용 해석:

- 공식 JSON의 `version`과 `data`를 그대로 출처 정본으로 삼을 수 있다.
- Data Dragon 자체가 특정 시점의 실제 지역 클라이언트 상태를 완전히 증명하지는 않는다. 따라서 “시즌 3 역사 스냅샷 후보” 이상의 주장을 하려면 당시 공식 패치·클라이언트 자료와 추가 대조가 필요하다.

### 2.4 현재 League of Legends Classic 공식 페이지

- 발행자: Riot Games
- URL: https://www.leagueoflegends.com/en-us/classic/
- 신뢰도: 높음 — 현행 제품 공식 페이지

확인된 사실:

- 현재 Classic은 초기 시대의 챔피언·아이템·시스템을 되살린다고 설명한다.
- 개발이 계속되며 플레이어 투표로 어떤 챔피언·아이템·기타 요소가 다음에 돌아올지 정한다고 설명한다.

제품 적용 해석:

- 현행 Classic은 단일 역사 패치를 그대로 고정 복제한 제품이라고 볼 근거가 없다.
- `3.13.24`는 역사 자료의 단일 기준선 후보일 뿐, 현행 Classic의 챔피언 풀·아이템·룬·특성·수치와 동일하다고 주장하면 안 된다. 현행 대응 여부는 `확인 중`이다.

## 3. 브랜딩·이미지·수익화 판정

| 항목 | 판정 | 구현 지침 |
|---|---|---|
| 개인 무료 팬 정보 페이지 | 조건부 진행 가능 | 정책 고지, Portal 등록·감사, 비공식성, 비상업 운영을 유지한다. |
| `lol-classic-hub` 공개 제품명/도메인/소셜 식별자 | 안전 판정 아님 | 일반 명칭과 일반 slug로 교체한다. Riot 표장을 SEO 키워드로 등록하지 않는다. |
| Riot·League of Legends 로고 | 금지 | 사용하지 않는다. Press Kit 예외가 필요해도 별도 검토 전 포함하지 않는다. |
| Data Dragon JSON | 조건부 사용 가능 | 버전·로케일·출처·확인일과 현행성 한계를 표시한다. |
| Data Dragon JSON이 직접 참조하는 이미지 | 조건부 사용 가능 | 같은 `3.13.24` 경로만 사용하고 매니페스트로 URL·해시를 고정한다. |
| 제3자 위키·팬사이트 데이터/이미지 | 금지 | 출처 후보 탐색에만 쓰고 제품 데이터로 복제하지 않는다. |
| 광고·결제·후원·구독 | 현재 금지 | Portal 등록 및 `Approved`/`Acknowledged` 확인 후 별도 재검토한다. |
| 현재 Classic과 `3.13.24` 동일성 | 확인 중 | 동일하다고 쓰지 않고 현행 공식 자료가 확보될 때까지 분리한다. |

## 4. 단일 데이터셋 후보: `3.13.24/ko_KR`

### 선택 이유와 한계

- Riot 공식 `versions.json`에 `3.13.24`가 유효 버전으로 존재한다.
- 동일 버전·동일 로케일에서 챔피언·아이템·룬·마스터리 네 파일이 모두 HTTP 200으로 제공되고 각 JSON의 `version`이 `3.13.24`다.
- 한국어 페이지이므로 우선 로케일은 `ko_KR`로 고정한다. 번역이 의심스러워도 `en_US` 또는 다른 패치와 필드 단위로 섞지 않는다. 대조가 필요하면 별도 검증 열에만 기록한다.
- 이 선택은 여러 패치의 수치를 혼합하지 않기 위한 **재현 가능한 기준선 후보**다. “시즌 3의 최종 정답” 또는 “2026 Classic 현행 데이터”라는 뜻이 아니다.

### 2026-08-02 실측

| 영역 | 공식 URL 응답 | JSON `version` | 레코드 수 | 출처 신뢰도 | 제품 적용 신뢰도 |
|---|---:|---:|---:|---|---|
| 챔피언 | HTTP 200 | `3.13.24` | 116 | 높음 | 역사 스냅샷: 높음 / 현행 Classic: 확인 중 |
| 아이템 | HTTP 200 | `3.13.24` | 205 | 높음 | 역사 스냅샷: 높음 / 현행 Classic: 확인 중 |
| 룬 | HTTP 200 | `3.13.24` | 296 | 높음 | 역사 스냅샷: 높음 / 현행 Classic: 확인 중 |
| 특성(마스터리) | HTTP 200 | `3.13.24` | 56 | 높음 | 역사 스냅샷: 높음 / 현행 Classic: 확인 중 |

레코드 수는 콘텐츠 완전성의 법률적·역사적 증명이 아니라 다운로드·파싱 재현성을 확인하는 운영 지표다.

### 수집·검증·인용 방식

1. 수집 시작 시 `versions.json`에 `3.13.24`가 있는지 확인한다.
2. 위 네 `ko_KR` JSON을 공식 HTTPS URL에서 내려받는다.
3. 원본 파일의 URL, 확인 시각, 바이트 수, SHA-256을 매니페스트에 기록한다.
4. 각 JSON의 `version == "3.13.24"`를 검증하고, 화면에 노출하는 수치는 원본 필드에서 기계적으로 생성한다.
5. 이미지가 필요하면 JSON이 가리키는 Data Dragon 이미지 경로만 허용하고 각 파일의 URL·HTTP 상태·SHA-256을 기록한다.
6. 누락·HTTP 실패·파싱 실패·버전 불일치는 `확인 중` 또는 `unavailable`로 기록하고 배포에서 제외한다.
7. 페이지 또는 데이터 안내에 최소한 다음을 표시한다.
   - `출처: Riot Games Data Dragon`
   - `버전/로케일: 3.13.24 / ko_KR`
   - `확인일: 2026-08-02`
   - `시즌 3 역사 스냅샷 후보이며 현재 League of Legends Classic과의 일치 여부는 확인 중`
   - 위 두 정책 고지 원문

## 5. 구현 금지사항 체크리스트

- [ ] 모델 기억으로 수치·효과·비용·쿨다운을 작성하지 않는다.
- [ ] 다른 Data Dragon 버전 또는 `en_US` 값을 `ko_KR` 레코드에 혼합하지 않는다.
- [ ] 위키·블로그·검색 결과를 유일 근거로 사용하지 않는다.
- [ ] 누락 이미지를 현대 에셋이나 비공식 에셋으로 대체하지 않는다.
- [ ] 현행 Classic과 `3.13.24`가 동일하다고 표현하지 않는다.
- [ ] Riot·League of Legends 로고나 공식 사이트를 모사한 UI를 쓰지 않는다.
- [ ] Riot 표장을 공개 제품명·도메인·소셜 계정·검색 태그에 넣지 않는다.
- [ ] Portal 등록·제품 상태 재검토 전 수익화를 켜지 않는다.
- [ ] 정책 고지와 출처·버전·현행성 한계를 숨기지 않는다.

## 6. 남은 확인 사항

- Developer Portal 제품 등록·감사 완료 여부: 확인 중
- 사용자 노출 제품명과 공개 URL의 일반 명칭 전환: 확인 중
- `3.13.24`와 현행 Classic 각 항목의 일치 여부: 확인 중
- 공개 직전 Riot 정책 변경 여부: 확인 중

위 항목은 데이터 페이지 구현을 위한 역사 스냅샷 준비를 막지는 않지만, 공개 배포·브랜딩·수익화 게이트에서는 완료 여부를 별도로 확인해야 한다.
