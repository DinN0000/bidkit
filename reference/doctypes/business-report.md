# Doctype: business-report — 사업/경영 보고 (의사결정 제안서)

개인·팀이 의사결정자에게 "이 안을 승인하라"고 제안하는 문서. 사업 검토 보고,
투자·도입 품의, 전략 보고 등 — 결재라는 결정을 받아내는 제안이다.

## Persuasion Frame

| Element | Value |
|---------|-------|
| 제안 주체 | 개인 또는 팀 (실무 조직) |
| 청중 | 의사결정자 — 경영진, 결재권자, 운영위원회 |
| 요청하는 결정 | 승인 — "이 안(권고안)을 채택하라" |
| 청중의 평가 기준 | 의사결정 기준 — 비용, 효과(ROI), 리스크, 전략 정합성, 시급성 |
| 전략 프레임 | 권고안 채택 전략 — 대안 대비 권고안의 우위를 기준별로 입증 |

## Input (at `/bid:design`)

- 보고 목적과 요청할 결정 (1문장으로 확정 — "무엇을 승인받으려는 보고인가")
- 의사결정자가 누구인지, 그가 중시하는 기준
- 근거 데이터 (내부 지표, 시장 자료, 비용 산정 근거)

## Criteria Trace Matrix

- 파일: `proposal/.bidkit/meta/criteria-trace-matrix.md` (`templates/init/criteria-trace-matrix.md`)
- 행 의미: 의사결정 기준 (비용/효과/리스크/...) → 다루는 SSOT → 커버리지
- 의사결정자가 반드시 물어볼 질문에 답이 없으면 coverage = none

## Team Composition

단일 팀 — Team Lead + Writer + Critic 기본. Researcher는 외부 데이터·벤치마크가
필요할 때만 투입. Overseer는 다중 섹션 보고서일 때만 cross-review 수행
(단일 섹션 보고는 Critic PASS + 사용자 확인으로 종결 가능 — Lite Loop).

## Section Structure Pattern

- 표준 구조: 보고 개요(요청 결정 명시) → 배경·현황 → **옵션 비교** (대안 2-3개,
  기준별 비교표) → 권고안 + 근거 → 실행 계획 (일정·비용·담당) → 리스크와 대응
- Executive Summary 우선 — 의사결정자가 1페이지만 읽어도 결정 가능해야 함
- 옵션 비교는 반드시 표 — 평가 기준을 행으로, 옵션을 열로

## Critic Checks

| # | Check | 적용 |
|---|-------|------|
| 1 | Audience criteria coverage | **ON** — 의사결정 기준 (criteria-trace-matrix) |
| 2 | Data accuracy | ON — 수치·산식·출처 검증 |
| 3 | Gap analysis | ON — 특히 "결정에 필요한데 빠진 정보" 검출 |
| 4 | Cross-SSOT consistency | ON (다중 섹션일 때) |
| 5 | Glossary compliance | ON |
| 6 | Regulatory compliance | **조건부** — 보고 주제가 규제 관련일 때만 |
| 7 | Style compliance (개조식) | **ON — 보고서는 개조식이 기본** |
| 8 | Internal redundancy | ON |

## Session Loop

**Lite** — Writer 초안 → Critic 검증 → 수정 → 사용자 확인. Overseer cross-review는
다중 섹션 보고서에만 적용. 정기 보고처럼 반복 작성 시 직전 버전을 `existing`
상태로 불러와 Enhance 모드로 진행.

## Researcher Focus

대안 조사 (경쟁 솔루션, 타사 사례), 내부 데이터 검증, 비용·효과 벤치마크,
의사결정자의 과거 결정 패턴·중시 기준 (가능한 범위에서)

## Default Output

MD + PDF (결재 첨부용). Executive Summary 1장 동시 생성
(`playbooks/output/SKILL.md`의 Executive Summary 플로우 기본 적용).
