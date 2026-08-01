# AIW-183 Data Dragon 공개 재개 판정 보고서

확인일: 2026-08-02 (KST)
판정: **개인 비상업 팬 프로젝트 경로로 공개 가능 — Data Dragon 3.13.24/ko_KR 통합·배포 진행**

> 이 문서는 법률 자문이 아니다. Riot Games의 공개 정책을 근거로 한 출시 전 운영 검토다.

## 1. 운영 주체 — 확인된 사실

사용자가 다음 사실을 명시적으로 확인했다.

- `ai-worker-lab`은 개인 비상업 프로젝트를 정리·운영하기 위한 GitHub Organization이다.
- 등록 사업체나 법인이 아니다.
- `클래식 노트`는 개인 비상업 무료 팬 프로젝트다.
- 광고·결제·후원·유료 기능이 없고 현재 수익화 계획이 없다.
- Riot 공식 서비스로 혼동될 표현과 Riot 로고를 사용하지 않는다.

따라서 이전 판정의 “사업·법인 관여 여부 불명확” 전제는 해소됐다.

## 2. 공식 정책 — 확인된 사실

### 2.1 `Legal Jibber Jabber`

- 발행자: Riot Games
- 표시 버전: Last Updated: August 2018
- URL: https://www.riotgames.com/en/legal

개인 비상업 커뮤니티 사용에 대한 조건부 허용:

> “Riot Games ... grants you a personal, non-exclusive, non-sublicenseable, non-transferable, revocable, limited license ... strictly for noncommercial ... community use.”

사업·법인 관여 프로젝트 제한:

> “You may not create commercial Projects, including ... any Project that involves a business or legal entity ... without a written license agreement from us.”

공유 시 필수 고지:

> “[The title of your Project] was created under Riot Games' ‘Legal Jibber Jabber’ policy using assets owned by Riot Games. Riot Games does not endorse or sponsor this project.”

로고·상표 제한: 서면 라이선스가 없으면 Riot 로고·상표를 사용할 수 없고 Riot과의 연계를 혼동시키면 안 된다.

### 2.2 `General Policies`

- 발행자: Riot Games Developer Relations
- 표시 버전: LAST UPDATED: MARCH 11, 2025
- URL: https://developer.riotgames.com/policies/general

확인된 원문:

- 제품 개발·마케팅에 사용할 자산으로 **Data Dragon**을 열거한다.
- 눈에 띄는 위치에 다음 비공식 제품 고지를 요구한다.

> “[Your product] isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.”

- 제품 등록 의무:

> “All products must be registered in, and audited by Riot Games through the Developer Portal.”

### 2.3 `League of Legends` — Data Dragon

- 발행자: Riot Games Developer Relations
- URL: https://developer.riotgames.com/docs/lol#data-dragon

> “Data Dragon provides two kinds of static data: data files and game assets.”

### 2.4 `League of Legends Classic`

- 발행자: Riot Games
- URL: https://www.leagueoflegends.com/en-us/classic/

공식 페이지는 original champions, items, systems를 소개하고, 향후 플레이어 투표로 챔피언·아이템·기타 요소가 추가될 수 있음을 설명한다. 단일 역사 패치의 완전 복제라는 설명은 확인되지 않았다.

## 3. 제품 적용 해석

### 공개 가능 판정

- 운영 주체가 개인 비상업으로 확정되어 `business or legal entity` 제한의 사실 전제가 없다.
- Data Dragon은 Developer General Policies가 허용 자산으로 명시한다.
- 무료·비상업 팬 프로젝트의 Data Dragon 공유를 직접 금지하는 별도 조항은 확인되지 않았다.
- 두 필수 고지, 비공식 브랜딩, 로고 미사용, 비수익화, 출처·버전·확인일 표시 조건을 구현한다.

따라서 막연한 법률 우려로 공개 게이트를 유지하지 않고 `public_distribution=true`로 전환한다.

### 잔여 운영 의무

Developer Portal 등록·감사는 명시적 정책 의무이며 아직 완료 증거가 없다. 사용자 인증이 필요한 후속 운영 작업으로 병행 추적하고, 완료 전에는 등록됐다고 주장하지 않는다. Riot은 정책에 따라 사용 허용을 철회할 수 있으므로 감사 결과와 정책 변경을 반영해야 한다.

## 4. 데이터 버전 단일화

### 비교 결과

| 기준 | 3.13.24 | 3.15.5 |
|---|---:|---:|
| 챔피언 | 116 | 117 |
| 아이템 | 205 | 220 |
| 룬 | 296 | 296 |
| 특성 | 56 | 57 |

`3.15.5`에는 `3.13.24`에 없는 Yasuo, 장신구, 프리시즌 지원 아이템과 교체된 특성 체계가 포함된다. 따라서 시즌 3 역사 기준선에는 부적합하다.

### 채택

- 공개 단일 버전: `3.13.24`
- 표시 로케일: `ko_KR`
- 이미지: locale-free `3.13.24` 공식 Data Dragon 아이콘
- 제품 표현: “시즌 3 역사 스냅샷”, “2026 League Classic 현행 동일성 미보증”

## 5. 데이터·에셋 무결성

### 기존 AIW-173 검증

- 데이터셋 4개 + 에셋 참조 673개 = 매니페스트 참조 677개
- 고유 공식 URL 451개
- 원격 HTTP 200 `451/451`
- 원격 SHA-256 일치 `451/451`
- 로컬 SHA-256 일치 `677/677`
- 에셋 참조 673개, 고유 이미지 447개
- 마스터리 트리 배경·연결선은 공식 아카이브 미제공으로 제외

### 공개 `ko_KR` JSON

| 파일 | 개수 | SHA-256 |
|---|---:|---|
| champion.json | 116 | `d073d5a023cb700118c3d63652b15d11fb8e213896897828cc024daef0cea925` |
| item.json | 205 | `cecc6ed683f80f076f0888053648f9604017155a9f9cc3ad2d9b47c3f8254bbe` |
| mastery.json | 56 | `2fd552d4fbf4cb25b5b4e1ba6e7bd7e7a3ba1dc1a63cbfe3fef34e57385a53ae` |
| rune.json | 296 | `de3d476f130bacd46e122acbc9a5a95fa2a1af94c8fce1d422297b1de795857f` |

## 6. 구현·로컬 검증

- AIW-173 에셋 커밋을 공개 작업 브랜치에 통합했다.
- 빌드가 4종 JSON을 읽어 항목 카드와 공식 아이콘을 생성한다.
- 모든 페이지에 두 필수 고지, 출처·버전·로케일·확인일·현행성 한계를 표시한다.
- Riot 로고·공식 서비스 혼동·수익화 코드·비공식 에셋을 포함하지 않는다.
- 사용자 노출 제품명과 메타 제목은 일반 명칭 `클래식 노트`로 통일했다. `lol-classic-hub`는 GitHub Pages 등록 도메인이 아니라 기존 저장소 경로이며, Portal 감사에서 변경 요청이 오면 일반 slug로 이전한다.
- 독립 사전 커밋 리뷰가 지적한 동반 변조 허점을 교정해, 공개 JSON은 알려진 공식 SHA-256에 고정하고 vendor 원본·site 복사본 이미지는 AIW-173 매니페스트의 673개 SHA-256과 직접 대조한다.

검증 결과:

```text
검증 성공: 페이지 6개, 오류 0건
데이터 항목: champions=116, items=205, masteries=56, runes=296
이미지: 참조 673개, 고유 파일 447개, vendor/site 누락·추가 0
정책: 필수 고지·비수익화·공식 이미지 경로·Riot 로고 미사용 확인
SEO: canonical/description/Open Graph/JSON-LD/robots/sitemap 확인
```

로컬 HTTP 검증:

- 홈·챔피언·아이템·룬·특성·빌더·robots·sitemap: HTTP 200
- 이미지 태그: 챔피언 116, 아이템 205, 룬 296, 특성 56
- 표본 이미지 `Aatrox.png`: HTTP 200, `image/png`, 14,055 bytes

## 7. 배포 결과

- 공개 URL: https://ai-worker-lab.github.io/lol-classic-hub/
- main 통합 커밋과 GitHub Actions 실행 결과는 배포 완료 후 이 문서와 AIW-183 이슈에 기록한다.

## 8. 후속 질문·운영 작업

- 프로젝트 소유자: 후속 이슈 AIW-184에서 Riot Developer Portal 제품 등록·감사를 완료하고 결과를 기록한다.
- 운영자: Riot 정책 변경 또는 감사 피드백이 있으면 공개 범위와 고지를 갱신한다.
- 데이터 운영: 2026 League Classic 현행 수치는 Riot 공식 근거가 확보되기 전까지 별도 사실로 단정하지 않는다.
