# Doctype: proposal — B2B 제안서

회사가 발주사에게 "우리를 선택하라"고 제안하는 문서. BidKit의 원형 doctype이며,
다른 프로필이 명시적으로 바꾸지 않는 한 모든 기본 동작은 이 프로필을 따른다.

## Persuasion Frame

| Element | Value |
|---------|-------|
| 제안 주체 | 회사 (제안 컨소시엄 포함) |
| 청중 | 발주사 평가위원회 |
| 요청하는 결정 | 수주 — "우리를 선택하라" |
| 청중의 평가 기준 | RFP 요구사항 + 평가 배점표 |
| 전략 프레임 | Win strategy — 경쟁사 대비 차별화 |

## Input (at `/bid:design`)

- RFP 문서 (PDF/DOCX/PPTX) — 필수에 준함
- 경쟁 구도, 자사 강점, 제약 조건 (대화로 수집)

## Criteria Trace Matrix

- 파일: `proposal/.bidkit/meta/rfp-trace-matrix.md` (`templates/init/rfp-trace-matrix.md`)
- 행 의미: RFP 요구사항 ID → 담당 SSOT → 커버리지 (full/partial/none)

## Team Composition

| Team | Domain |
|------|--------|
| BA | 요구사항, 프로세스, 비용 산정 |
| DA | 데이터 모델, 이행, 데이터 보안 |
| TA | 인프라, 플랫폼, 사이징 |
| SA | 제품 사양, 솔루션 설계, 경쟁 포지셔닝 |

구조 패턴: `reference/domain/{ba|da|ta|sa}.md`

## Critic Checks

| # | Check | 적용 |
|---|-------|------|
| 1 | Audience criteria coverage | **ON** — RFP 요구사항 기준 |
| 2 | Data accuracy | ON |
| 3 | Gap analysis | ON |
| 4 | Cross-SSOT consistency | ON |
| 5 | Glossary compliance | ON |
| 6 | Regulatory compliance | **ON** — 금융보안원, 망분리 등 (규제 산업 발주 기준) |
| 7 | Style compliance (개조식) | ON |
| 8 | Internal redundancy | ON |

## Session Loop

Full — 10단계 전체 (`skills/write/SKILL.md`). Researcher·Critic·Overseer 모두 참여.

## Researcher Focus

경쟁사 접근 방식, 제품 사양·인증, 레퍼런스 사례, 규제 요건, 가격 범위

## Default Output

MD (항상) + PPT/PDF (발주사 제출 양식에 따름)
