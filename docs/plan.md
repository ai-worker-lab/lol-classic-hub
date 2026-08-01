# AIW-168 구현 계획

## 요약

외부 프레임워크와 런타임 의존성을 제거한 정적 사이트를 Python 표준 라이브러리 생성기로 만든다. Riot IP 출시 게이트가 해제되기 전에는 Data Dragon `3.15.5` 출처 후보와 `확인 중` 상태만 표시하고 실제 게임 데이터·이미지는 배포하지 않는다. GitHub Actions의 공식 Pages 액션으로 중립 정적 셸을 무료 배포한다.

## 기술 맥락

- 언어: HTML5, CSS, 브라우저 JavaScript, Python 3 표준 라이브러리
- 호스팅: GitHub Pages (`https://ai-worker-lab.github.io/lol-classic-hub/`)
- 출처 후보: `https://ddragon.leagueoflegends.com/cdn/3.15.5/data/ko_KR/*.json` (정책 게이트 해제 전 미수집·미노출)
- 저장 도구: 브라우저 `localStorage`, 서버·계정 없음
- 배포: `actions/configure-pages`, `actions/upload-pages-artifact`, `actions/deploy-pages`

## Constitution Check

- Spec-first: `docs/spec.md`를 코드 전에 작성했다.
- 출처 우선: 모델 기억의 게임 수치를 사용하지 않는다.
- 최소 변경: 신규 빈 저장소에 MVP 범위 파일만 추가한다.
- 무료 운영: 유료 API·서버·DB·도메인을 사용하지 않는다.
- 안전: 비밀 정보를 코드·로그·페이지에 포함하지 않는다.
- 범위 제한: 커뮤니티와 모든 Riot 게임 데이터·이미지 에셋을 제외한다. 정책 게이트 해제 전에는 중립 셸과 사용자 직접 입력 메모만 제공한다.

## 프로젝트 구조

```text
.github/workflows/pages.yml  GitHub Pages 배포
scripts/build.py             공식 JSON 기반 정적 페이지 생성
scripts/verify.py            링크·SEO·출처 정적 검증
site/                        배포 산출물
  assets/                    CSS와 빌더 JS
  runes/ ...                 고유 레퍼런스 URL
  builder/                   로컬 저장 빌더
  robots.txt, sitemap.xml
  404.html
README.md                    운영 런북
```

## 검증

1. `python3 scripts/build.py`
2. `python3 scripts/verify.py` (게임 데이터·에셋 미노출 게이트 포함)
3. `python3 scripts/serve.py`에서 HTTP 200 확인
4. Playwright 또는 브라우저 JavaScript로 저장·재로드·삭제 확인
5. push 후 GitHub Actions 성공 확인
6. 공개 URL의 홈, 핵심 URL, robots, sitemap을 `curl`로 확인

## 복잡성 추적

- 정적 생성기를 도입한 이유: 출처 버전과 확인일을 한 곳에서 강제하고 데이터 갱신을 재현 가능하게 하기 위함이다.
- 정책 승인 전 데이터셋을 강제로 비워 잘못된 현행성 주장과 무허가 Riot IP 공개 위험을 줄인다. 승인 후 별도 변경에서 출처·버전·허용 범위를 검증하고 데이터를 추가한다.
