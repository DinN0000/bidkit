# Doctype: portfolio — 포트폴리오 (개인의 자기 제안서)

개인이 회사·클라이언트에게 "나를 선택하라"고 제안하는 문서. 채용, 프리랜스 계약,
사내 발탁 등 — 청중과 평가 기준이 있다는 점에서 구조적으로 제안서와 동일하다.

## Persuasion Frame

| Element | Value |
|---------|-------|
| 제안 주체 | 개인 (또는 소규모 팀/스튜디오) |
| 청중 | 채용 담당자, 클라이언트, 발탁 결정권자 |
| 요청하는 결정 | 채용·계약 — "나를 선택하라" |
| 청중의 평가 기준 | JD·공고 요구사항, 평가 항목 (없으면 타깃 직무·시장 기준) |
| 전략 프레임 | Positioning — 타 후보 대비 차별화 포인트 1-2개에 집중 |

## Input (at `/bid:design`)

- 프로젝트 실적 자료 (이력서, 프로젝트 기록, 성과 데이터, 링크)
- 타깃: 지원할 회사/직무의 JD 또는 공고 (있으면 trace matrix의 기준이 됨)
- 타깃이 불특정이면: 목표 직무·포지셔닝을 대화로 정의

## Criteria Trace Matrix

- 파일: `proposal/.bidkit/meta/criteria-trace-matrix.md` (`templates/init/criteria-trace-matrix.md`)
- 행 의미: JD·공고 요구 역량 → 입증하는 케이스 스터디 SSOT → 커버리지
- JD가 없으면 타깃 직무의 일반 요구 역량으로 행을 구성

## Team Composition

단일 팀 — Team Lead + Writer + Researcher + Critic (Overseer는 전체 포지셔닝
일관성 리뷰 담당). BA/DA/TA/SA 분할 없음. `reference/domain/*.md` 미적용.

## Section Structure Pattern

- **케이스 스터디 단위 SSOT**: 프로젝트 1개 = SSOT 1개
- 케이스 스터디 6단계 구조 (순서 고정):

| 단계 | 내용 |
|------|------|
| 1. 문제정의 (Problem) | 무엇이 왜 문제였는지 — 비즈니스·사용자 맥락, 본인의 역할과 책임 범위 |
| 2. 가설 (Hypothesis) | 어떤 접근이 문제를 풀 것이라 판단했는지 — 검토한 대안과 선택 근거 |
| 3. 실행 (Execution) | 실제로 한 일 — 기술, 핵심 의사결정, 본인 기여분 명시 (팀 작업과 구분) |
| 4. 검증 (Validation) | 가설이 맞았는지 어떻게 확인했는지 — 실험 설계, 측정 방법, 중간 피벗 |
| 5. 임팩트 (Impact) | 수치화된 성과 — 비즈니스·기술 지표의 before → after |
| 6. 러닝 (Learning) | 배운 것, 다시 한다면 달리할 것 — 다음 프로젝트에 전이된 교훈 |

- 이 구조 자체가 설득 장치 — 결과 나열이 아니라 문제 해결 사고 과정을 입증
- 공통 섹션: 프로필 요약(포지셔닝 선언), 기술 스택, 경력 타임라인, 연락처
- 임팩트는 반드시 수치화 — "성능 개선" (×) → "p95 지연시간 2.1s → 340ms" (○)

## Critic Checks

| # | Check | 적용 |
|---|-------|------|
| 1 | Audience criteria coverage | **ON** — JD·공고 요구 역량 기준 (criteria-trace-matrix) |
| 2 | Data accuracy | ON — 수치·기간·역할 표기의 사실성 |
| 3 | Gap analysis | ON — 주장만 있고 입증 케이스 없는 역량 검출 + 6단계 구조 누락 검출 (특히 검증·임팩트 없는 케이스는 Warning) |
| 4 | Cross-SSOT consistency | ON — 케이스 간 기간·역할·기술 명칭 일치 |
| 5 | Glossary compliance | ON — 기술 용어·제품명 표기 통일 |
| 6 | Regulatory compliance | **OFF** — 단, 전 고용주 기밀·NDA 위반 소지 검출은 수행 |
| 7 | Style compliance (개조식) | ON — 프로필 요약 등 산문 관례 섹션은 `style: prose` 지정 가능 |
| 8 | Internal redundancy | ON — 같은 성과를 여러 케이스에서 중복 주장하지 않음 |

## Session Loop

Full — 단, 팀이 하나이므로 병렬 분업 없이 케이스 스터디 단위로 순차 진행.

## Researcher Focus

타깃 회사·직무 분석 (JD 키워드, 기술 스택, 조직 맥락), 동일 직군 포트폴리오
벤치마크, 본인 실적 데이터의 수치 검증 (커밋 기록, 지표 대시보드, 발표 자료)

## Default Output

HTML 정적 사이트 (기본 — 링크 공유·탐색에 최적) + PDF (지원서 첨부용)
