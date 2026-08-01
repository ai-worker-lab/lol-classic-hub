# 시즌3 Riot Data Dragon 에셋

AIW-173의 재현 가능한 조사·보관 산출물이다. 공식 Data Dragon 이외의 CDN이나 출처 불명 파일은 사용하지 않는다.

## 선택 버전

- 공식 버전 목록: `https://ddragon.leagueoflegends.com/api/versions.json`
- 선택: `3.13.24` / `en_US`
- 근거: 공식 목록에서 접근 가능한 3.x 아카이브 중 3.13 계열의 최종 빌드다. 3.14 이상은 시즌 종료 뒤 프리시즌 변경을 포함할 가능성이 있어 보수적으로 제외했다.
- 원본 데이터: `upstream/3.13.24/data/en_US/*.json`
- 이미지: `vendor/riot-data-dragon/3.13.24/img/{champion,item,rune,mastery}/`
- 항목별 출처·버전·확인일·SHA-256: `manifest.json`

## 재현

Python 표준 라이브러리만 사용한다. `--checked-at`은 조사 시각을 명시적으로 고정해 같은 입력에서 매니페스트가 불필요하게 바뀌지 않게 한다.

```bash
python3 assets/fetch_data_dragon.py \
  --checked-at 2026-08-01T16:24:52Z
```

스크립트는 다음을 검증한다.

1. 공식 `versions.json`에 `3.13.24`가 존재하는지 확인한다.
2. `champion.json`, `item.json`, `rune.json`, `mastery.json`을 공식 URL에서 받는다.
3. 각 데이터가 가리키는 개별 이미지만 공식 Data Dragon URL에서 받는다.
4. 항목별 HTTP 상태, 파일명, 크기, SHA-256을 `manifest.json`에 기록한다.
5. 공식 URL이 실패한 항목은 추정·대체하지 않고 `unavailable`로 기록한다.

## 상태와 공개 배포 게이트

- `availability: available`: 공식 URL 응답과 로컬 파일 SHA-256을 확인했다.
- `availability: unavailable`: 공식 데이터가 파일을 제공하지 않거나 공식 URL 접근에 실패했다. 임의 복제·현대 자산 대체 금지.
- `policy_status: 공개 가능 (조건부)`: 2026-08-02 개인 비상업 팬 프로젝트 사실관계와 Riot 공식 정책을 재검토했다.
- `public_distribution: true`: 두 필수 고지, 공식 출처·버전·확인일, Riot 로고 미사용, 비수익화 조건으로 공개한다.
- `mastery_tree_chrome`: 공식 아카이브 미제공으로 계속 제외한다.
- Developer Portal 제품 등록·감사는 AIW-184에서 공개와 병행한다.

정책 확인 출발점:

- Riot Developer Portal Data Dragon 문서: `https://developer.riotgames.com/docs/lol#data-dragon`
- Riot 법률 문서 포털: `https://www.riotgames.com/en/legal`

`mastery.json`과 56개 마스터리 아이콘은 공식 3.13.24 아카이브에서 확인했다. 반면 마스터리 트리 배경·연결선용 별도 파일은 데이터에서 URL을 제공하지 않으므로 `manifest.json`의 `not_provided_by_archive`에 `unavailable`로 남겼다.
