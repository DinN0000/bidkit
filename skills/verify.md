# /verify — Cross-SSOT Consistency Check

## Trigger

`/verify` command or natural language like "교차 검증해줘"

---

## Prerequisites

1. **Project exists** — `meta/proposal-meta.yaml` must exist. If not, redirect: *"프로젝트가 아직 없습니다. `/design`으로 먼저 시작할까요?"*
2. **Outline loaded** — `meta/outline.yaml` must exist. If not, redirect to `/design`.
3. **Minimum SSOTs** — at least 2 SSOTs must have `status` of `confirmed` or `tentative`. If fewer exist, inform: *"교차 검증에는 최소 2개의 확인/잠정 섹션이 필요합니다. 더 많은 섹션을 작성한 후 다시 시도해 주세요."*

---

## How /verify Differs from Automatic Overseer Review

`/verify` is BROADER than the automatic Overseer review that happens in step (10) of the `/write` session loop:

| | Automatic Overseer Review | /verify |
|---|---|---|
| **Trigger** | Automatic on tentative status | User-initiated on demand |
| **Scope** | Single SSOT vs its dependencies | ALL confirmed/tentative SSOTs |
| **Focus** | Does this SSOT fit the whole? | Cross-cutting issues across the whole |
| **Checks** | Terms, data, strategy alignment | + Redundancy, gaps, narrative flow |

---

## Flow

### Step (1) — Collect All Eligible SSOTs

1. Read `meta/outline.yaml` for section ordering and team assignments.
2. Read all SSOT files under `ssot/` and filter to those with `status` in: `confirmed`, `tentative`.
3. Also include SSOTs with `status: draft`, `verified`, or `reviewing` if they exist — these are checked but flagged as potentially incomplete.
4. Read `meta/glossary.yaml` for the authoritative term list.
5. Read `meta/rfp-trace-matrix.md` for requirement coverage mapping.
6. Read `meta/proposal-meta.yaml` for project context.

### Step (2) — Overseer Cross-Analysis

The Overseer performs a comprehensive cross-analysis across ALL collected SSOTs. This analysis covers five dimensions:

#### 2a. Terminology Consistency

Check all SSOTs for consistent use of terms:

- **Server names** — the same server must be referred to by the same name everywhere (e.g., "HSM 서버" vs "보안 서버" vs "HSM Server").
- **Product names** — exact product names, model numbers, and version strings must match across sections.
- **Abbreviations** — abbreviations must be defined on first use and used consistently. Check against `meta/glossary.yaml`.
- **Organization names** — customer, partner, and vendor names must be identical everywhere.
- **Technical terms** — domain-specific terms must match the glossary definition.

For each inconsistency found, record:
- The term variants found
- Which SSOTs use which variant
- The recommended canonical form (from glossary if available)

#### 2b. Data Accuracy

Check that numerical data is consistent across all SSOTs:

- **Server counts** — total servers, per-type counts match between architecture and cost sections.
- **Cost figures** — unit prices, totals, subtotals are arithmetically correct and consistent.
- **Performance metrics** — TPS, throughput, latency figures match between solution and architecture sections.
- **Sizing data** — storage, memory, CPU specifications match between solution specs and infrastructure plans.
- **Timeline data** — dates, durations, milestones are consistent between implementation plan and project overview.
- **Licensing** — license counts match server/user counts in other sections.

For each mismatch found, record:
- The conflicting values
- Which SSOTs contain each value
- Which value appears to be correct (with reasoning)

#### 2c. Redundancy Detection

Identify content that appears in multiple sections:

- **Exact duplicates** — identical paragraphs or tables in multiple SSOTs.
- **Near duplicates** — substantially similar content with minor variations (more dangerous than exact copies as they may diverge).
- **Appropriate vs inappropriate** — some redundancy is intentional (e.g., executive summary repeating key points). Flag only inappropriate redundancy.

For each redundancy found, record:
- The duplicated content summary
- Which SSOTs contain it
- Whether it is appropriate or should be consolidated
- Recommendation: which SSOT should own the content

#### 2d. Gap Analysis

Check that all RFP requirements are adequately covered:

- **Unmapped requirements** — requirements in `meta/rfp-trace-matrix.md` not assigned to any SSOT.
- **Mapped but unaddressed** — requirements assigned to a SSOT but not actually covered in its content.
- **Partial coverage** — requirements addressed but insufficiently (e.g., mentioned but not elaborated).
- **Orphan content** — substantial content in SSOTs that does not map to any RFP requirement (may indicate scope creep or missing RFP mapping).

For each gap found, record:
- The RFP requirement reference
- Current coverage status
- Which SSOT should address it
- Suggested action

#### 2e. Narrative Flow

Assess whether the sections tell a coherent story when read in outline order:

- **Logical progression** — does each section build on the previous one?
- **Transitions** — do sections reference or connect to adjacent sections?
- **Consistency of tone** — is the writing style consistent across sections?
- **Story arc** — does the proposal have a clear beginning (problem), middle (solution), and end (implementation + value)?
- **Strategic coherence** — do all sections support the same win strategy?

For each flow issue found, record:
- The nature of the disconnect
- Which sections are involved
- Suggested improvement

### Step (3) — Structured Report Output

Present the verification results in two layers:

1. **Decision List first** — what the user should decide or approve next
2. **Detailed report second** — grouped by severity for traceability

Decision List format:

```
### 지금 결정할 것

1. [필수] sa-hsm-001 서버 수량을 12대와 14대 중 어떤 값으로 확정할지 결정
2. [필수] 제품 표준 명칭을 glossary 기준으로 통일 승인
3. [권장] ta-infra-001의 중복 사양표를 참조 방식으로 바꿀지 승인
```

Then present the detailed report grouped by severity:

```
## Cross-SSOT Verification Report: [project name]

SSOTs analyzed: N (confirmed: N, tentative: N, other: N)

---

### Critical Issues (must fix before submission)

#### C-001: Data Mismatch — Server Count
- **Sections**: sa-hsm-001 (12 servers), ba-cost-001 (14 servers)
- **Impact**: Cost calculation will be wrong
- **Fix**: Confirm actual count and update both SSOTs

#### C-002: Terminology — Product Name
- **Sections**: sa-hsm-001 ("Luna Network HSM 7"), ta-infra-001 ("Thales Luna HSM")
- **Impact**: Appears inconsistent and unprofessional to evaluator
- **Fix**: Standardize to glossary term, update both SSOTs

---

### Warning Issues (should fix)

#### W-001: Redundancy — HSM Specification Table
- **Sections**: sa-hsm-001, ta-infra-001
- **Impact**: If one is updated without the other, data will diverge
- **Fix**: Keep detailed spec in sa-hsm-001, reference from ta-infra-001

#### W-002: Narrative Gap — Missing Transition
- **Sections**: Between ta-arch-001 and sa-impl-001
- **Impact**: Reader loses thread between architecture and implementation
- **Fix**: Add bridging paragraph in sa-impl-001 introduction

---

### Info Issues (optional improvement)

#### I-001: Abbreviation — "HA" Not Defined
- **Sections**: ta-infra-001 (first use without expansion)
- **Impact**: Minor — most evaluators will know the term
- **Fix**: Expand on first use: "고가용성(HA, High Availability)"

---

### Summary
- Critical: N issues across M SSOTs
- Warning: N issues across M SSOTs
- Info: N issues across M SSOTs
- RFP coverage: N/M requirements fully covered
```

### Step (4) — Action Items

After the report, present specific action items tied to SSOTs:

```
### Action Items / Revision Queue

| Priority | SSOT | Directive | Issues |
|----------|------|-----------|--------|
| 1 | sa-hsm-001 | Fix server count to match ba-cost-001, standardize product name | C-001, C-002 |
| 2 | ba-cost-001 | Update server count to match confirmed architecture | C-001 |
| 3 | ta-infra-001 | Remove redundant spec table, reference sa-hsm-001, fix product name, expand "HA" | C-002, W-001, I-001 |
| 4 | sa-impl-001 | Add bridging paragraph referencing ta-arch-001 architecture decisions | W-002 |
```

For each action item:
- The SSOT ID that needs revision
- A specific directive describing what to change
- Which issues from the report are addressed
- Priority order (Critical issues first, then Warning, then Info)

The user can then choose to:
- **Fix all** — process action items in priority order via `/write` sessions
- **Fix selected** — pick specific items to address
- **Defer** — acknowledge issues and return later

---

## Error Handling

### Project Not Found

If `meta/proposal-meta.yaml` does not exist:

```
프로젝트가 아직 없습니다. `/design`으로 프로젝트를 먼저 만들어 주세요.
```

### Insufficient SSOTs

If fewer than 2 SSOTs have `confirmed` or `tentative` status:

```
교차 검증에는 최소 2개의 확인/잠정 섹션이 필요합니다.
현재: confirmed N개, tentative N개
더 많은 섹션을 작성한 후 다시 시도해 주세요.
```

Then show Proposal Guide with recommendation to `/write` the next section.

### No Issues Found

If all checks pass with no issues:

```
교차 검증 완료 — 문제가 발견되지 않았습니다.
모든 섹션의 용어, 데이터, 서사 흐름이 일관됩니다.
```

---

## Key References

| File | Purpose |
|------|---------|
| `meta/outline.yaml` | Section ordering, team assignments, dependencies |
| `meta/proposal-meta.yaml` | Project name and metadata |
| `meta/glossary.yaml` | Authoritative term list for consistency checks |
| `meta/rfp-trace-matrix.md` | RFP requirement coverage mapping |
| `ssot/<team>/<id>.md` | Per-section SSOT files |
| `reference/proposal-guide-format.md` | Proposal Guide footer format |
| `reference/state-machine.md` | Valid SSOT states |
| `agents/overseer.md` | Overseer cross-review protocol |

---

## Proposal Guide

**Render at the bottom of every response** per `reference/proposal-guide-format.md`.

```
-------------------------------------------------
Project: [project name]
-------------------------------------------------
Current: [user-facing situation label]
Done: [v] section1 (team), [v] section2 (team)
In Progress: [~] section3 (team) -- current activity details
Recommended: /command copy-pasteable example input
-------------------------------------------------
```

### Status Icons

| Icon | Meaning |
|------|---------|
| [v] | confirmed |
| [~] | in progress (draft / verifying / verified / tentative / reviewing) |
| [>] | ideation |
| [ ] | not started |
| [!] | revision (Overseer directive or re-edit of confirmed) |

### Recommendation Logic

Show exactly ONE recommendation — the highest-priority match:

1. No project exists -> `/design`
2. Design complete, all SSOTs empty -> `/write <first priority section>`
3. Some sections in draft -> `/write` on incomplete section
4. 2+ sections confirmed -> `/verify`
5. All confirmed -> `/output` to generate final deliverable
6. Output generated, small change needed -> natural language quick edit
7. Versions available -> `/output diff` to compare versions
8. External input received -> natural language guidance
9. Ideation sections exist -> `/write <section>`
