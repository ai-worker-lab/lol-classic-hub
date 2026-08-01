# 클래식 노트 구현·운영 계획

## 요약

Python 표준 라이브러리 생성기가 공식 Data Dragon `3.13.24/ko_KR` JSON 4종을 읽어 정적 페이지를 만들고, 검증된 locale-free `3.13.24` 아이콘을 함께 배포한다. GitHub Actions가 main push마다 build/verify 후 GitHub Pages에 배포한다.

## 기술 맥락

- HTML5, CSS, 브라우저 JavaScript, Python 3 표준 라이브러리
- 데이터: `assets/upstream/3.13.24/data/ko_KR/*.json`
- 이미지: `assets/vendor/riot-data-dragon/3.13.24/img/**`
- 빌드: `scripts/build.py`
- 검증: `scripts/verify.py`
- 배포: GitHub Pages `https://ai-worker-lab.github.io/lol-classic-hub/`

## Constitution Check

- Spec-first: 운영 주체와 버전 결정을 구현 전에 spec에 반영한다.
- 출처 우선: 모델 기억이나 비공식 CDN을 사용하지 않는다.
- 추적성: 공식 URL·SHA-256·매니페스트·배포 SHA를 연결한다.
- 무료 운영: 유료 API·서버·DB·도메인을 사용하지 않는다.
- 범위 제한: 커뮤니티 기능·수익화·Riot 로고·비공식 에셋을 제외한다.

## 프로젝트 구조

```text
.github/workflows/pages.yml                 main → GitHub Pages
assets/upstream/3.13.24/data/ko_KR/        공개 데이터 SSoT
assets/vendor/riot-data-dragon/3.13.24/    공식 아이콘
scripts/build.py                            정적 생성기
scripts/verify.py                           데이터·에셋·고지·SEO 검증
site/                                       배포 산출물
docs/                                       명세·계획·작업·정책 판정
```

## 검증

1. `python3 scripts/build.py`
2. `python3 scripts/verify.py`
3. `python3 scripts/serve.py`에서 핵심 URL과 이미지 HTTP 확인
4. main push 후 GitHub Actions 성공 확인
5. 공개 URL에서 데이터 개수·고지·이미지·robots·sitemap 확인

## 복잡성 추적

- 데이터 레코드 673개가 고유 이미지 447개를 공유한다.
- `3.15.5`는 Yasuo·장신구·프리시즌 지원 아이템·교체 특성을 포함하므로 시즌 3 기준에서 제외한다.
- Developer Portal 등록·감사는 사용자 인증이 필요한 외부 운영 작업으로 별도 추적한다.
