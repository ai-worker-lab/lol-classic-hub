# AIW-183 Data Dragon 공개 판정 보고서

확인일: 2026-08-02 (KST)
판정: **공개 게이트 유지 — 구체적 정책 조항과 운영 주체 불명확성이 해소될 때까지 사이트 통합·재배포 금지**

> 이 문서는 법률 자문이 아니다. Riot Games의 공개 정책을 근거로 한 출시 전 운영 검토다.

## 1. 데이터·에셋 검증 — 확인된 사실

검증 대상은 AIW-173이 Riot 공식 CDN에서 확보한 Data Dragon `3.13.24` / `en_US`다.

- 공식 버전 목록: `https://ddragon.leagueoflegends.com/api/versions.json`
- 데이터셋: `champion.json`, `item.json`, `rune.json`, `mastery.json` 4종
- 매니페스트 참조: 데이터셋 4개 + 에셋 673개 = 677개
- 고유 공식 URL: 451개(데이터셋 4개 + 고유 이미지 447개)
- 재검증 결과: HTTP 200 `451/451`, 원격 SHA-256 일치 `451/451`
- 로컬 매니페스트 참조 SHA-256 일치 `677/677`, 누락·불일치 0
- 에셋 참조 분포: 챔피언 116, 아이템 205, 마스터리 56, 룬 296
- 동일 이미지를 여러 데이터 레코드가 참조하므로 에셋 참조 673개와 고유 이미지 447개가 다르다.
- 공식 아카이브가 별도 URL을 제공하지 않는 마스터리 트리 배경·연결선 1종은 `unavailable`이며 공개 대상에서 제외한다.

### 대상 버전 적합성

- 확인된 사실: `3.13.24`는 Riot 공식 버전 목록에 존재하는 3.x 역사 스냅샷이고, 4종 데이터와 연결 에셋이 공식 CDN에서 재현된다.
- 제품 적용 해석: 시즌3 말기 역사 레퍼런스의 출처로는 사용 가능하다.
- 한계: 이것이 2026 롤 클래식의 실제 챔피언 풀·룬·마스터리·아이템 수치와 정확히 같다는 Riot 공식 근거는 확보되지 않았다. 따라서 공개가 허용되더라도 **“시즌3 Data Dragon 역사 스냅샷”**으로 표시하고 현행 롤 클래식과 동일하다고 단정하면 안 된다.

## 2. 공식 정책 — 확인된 사실

### 2.1 Riot Games, `Legal Jibber Jabber`

- 발행자: Riot Games
- 표시 버전: Last Updated August 2018
- URL: `https://www.riotgames.com/en/legal`

무료 팬 프로젝트에 대한 조건부 허용 원문:

> “Riot Games ... grants you a personal, non-exclusive, non-sublicenseable, non-transferable, revocable, limited license ... strictly for noncommercial ... community use.”

사업·법인 관여 제한 원문:

> “You may not create commercial Projects, including ... any Project that involves a business or legal entity ... without a written license agreement from us.”

공유 시 고지 원문:

> “[The title of your Project] was created under Riot Games' ‘Legal Jibber Jabber’ policy using assets owned by Riot Games. Riot Games does not endorse or sponsor this project.”

로고·상표 제한 원문 요지: 서면 라이선스가 없으면 Riot 로고·상표를 프로젝트나 웹사이트에 사용할 수 없고 Riot과의 연계를 혼동시키면 안 된다.

### 2.2 Riot Developer, `General Policies`

- 발행자: Riot Games Developer Relations
- 표시 버전: LAST UPDATED: MARCH 11, 2025
- URL: `https://developer.riotgames.com/policies/general`

허용 자산 원문 요지: 제품 개발·마케팅에 사용할 자산으로 **Data Dragon**을 명시적으로 열거한다.

필수 고지 원문:

> “[Your product] isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.”

제품 등록 원문:

> “All products must be registered in, and audited by Riot Games through the Developer Portal.”

### 2.3 Riot Developer, `League of Legends` — Data Dragon

- 발행자: Riot Games Developer Relations
- URL: `https://developer.riotgames.com/docs/lol#data-dragon`

원문:

> “Data Dragon provides two kinds of static data: data files and game assets.”

문서는 버전·언어별 데이터 파일과 게임 에셋의 공식 URL 구조를 제공한다. 이 문서와 General Policies는 Data Dragon 자체를 허용된 정적 데이터/에셋 경로로 취급한다.

## 3. 제품 적용 해석

### 공개에 유리한 근거

- 무료·비상업 커뮤니티 팬 프로젝트는 `Legal Jibber Jabber`의 조건부 라이선스 대상이다.
- Riot Developer 정책은 Data Dragon을 제품에 사용할 수 있는 자산으로 명시한다.
- 현재 사이트는 광고·결제·후원·도박·API 키·사용자 계정이 없는 무료 정적 정보 사이트다.
- Riot 로고와 공식 UI를 사용하지 않고 중립 브랜드를 쓴다.

### 현재 공개를 막는 구체적 근거

공개 저장소와 Pages 호스트가 `ai-worker-lab` 조직에 속하고 업무 산출물이 AI Worker Lab 회사 프로젝트로 관리된다. `Legal Jibber Jabber`는 **사업 또는 법인이 관여하는 프로젝트를 상업 프로젝트에 포함**시키고, Riot의 서면 라이선스 없이는 이를 금지한다. AI Worker Lab의 실제 법적·사업 주체 여부가 확인되지 않았고 Riot 서면 라이선스나 제품 감사 결과도 기록돼 있지 않다.

이는 막연한 법률 우려가 아니라 위 2.1의 직접 원문에 따른 구체적 게이트다. 따라서 데이터 무결성이 완전하더라도 현재 상태에서 `public_distribution=true`로 바꾸지 않는다.

또한 General Policies의 “등록 및 감사” 의무가 충족됐다는 증거가 없다. 등록을 병행한다는 계획만으로 완료 상태를 주장할 수 없다.

## 4. 해제 절차와 담당자

### 경로 A — 개인 무료 팬 프로젝트로 운영

담당자: 프로젝트 소유자/CEO

1. AI Worker Lab이 사업·법인 관여 주체가 아님을 확인하거나, 프로젝트를 실제 개인 소유 저장소·호스팅으로 이전한다.
2. 회사·사업 홍보, 광고, 결제, 후원, 유료 기능을 넣지 않는다.
3. Developer Portal에 제품을 등록하고 최신 설명·공개 URL을 제출한다.
4. 페이지에서 아래 두 고지를 눈에 띄게 표시한다.
   - Developer General Policies의 비공식 제품 고지
   - `Legal Jibber Jabber`의 팬 프로젝트/에셋 소유 고지
5. Data Dragon `3.13.24`, 공식 출처 URL, 확인일, “시즌3 역사 스냅샷이며 2026 현행 일치 미확인” 문구를 표시한다.
6. Riot 로고·공식 UI·마스터리 트리 배경/연결선을 제외한다.

### 경로 B — AI Worker Lab 사업·법인이 계속 관여

담당자: 프로젝트 소유자/CEO 및 Riot Developer Relations

1. Developer Portal에 제품을 등록한다.
2. Riot에 `Legal Jibber Jabber`의 business/legal entity 조항을 명시해 이 무료 정적 팬 사이트의 허용 여부를 문의한다.
3. **서면 라이선스 또는 이 프로젝트에 적용 가능한 명시적 서면 승인**을 확보한다.
4. 제품 감사 결과와 허용 범위를 기록한 뒤에만 공개 게이트를 해제한다.

## 5. 공개 전 검증 체크리스트

- [ ] 운영 주체 경로 A 또는 B 확정
- [ ] Developer Portal 제품 등록·감사 증거 기록
- [ ] 필요한 경우 Riot 서면 라이선스/명시 승인 확보
- [ ] 두 필수 고지문을 눈에 띄게 표시
- [ ] Data Dragon 버전·출처·확인일·현행성 한계 표시
- [ ] Riot 로고·공식 UI·비공식 에셋 0건
- [ ] 광고·결제·후원 0건
- [ ] 마스터리 트리 배경·연결선 제외
- [ ] 빌드 검증·Pages 배포·공개 HTTP 검증

## 6. 현재 조치

- `public_distribution=false` 유지
- 사이트 데이터·이미지 에셋 노출 0건 유지
- 에셋 통합·Pages 재배포 미실행
- 기존 중립 정적 셸 공개 URL은 유지: `https://ai-worker-lab.github.io/lol-classic-hub/`

주의: AIW-173 에셋 브랜치는 공개 GitHub 저장소의 원격 브랜치에 이미 push된 상태이므로, “사이트 미노출”과 “파일 비공개”는 동일하지 않다. 원격 브랜치의 공개 상태를 별도 운영 리스크로 검토해야 한다.
