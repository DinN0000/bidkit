# /diagnose — Full Quality Diagnosis + Improvement

## Trigger

`/diagnose` command or natural language like "전체적으로 좀 약한 것 같아", "기존 제안서 있는데 전체적으로 봐줘", "교차 검증해줘", "일관성 확인해줘"

---

## Prerequisites

1. **Project exists** — `proposal/.bidkit/meta/proposal-meta.yaml` must exist. If not, redirect: *"프로젝트가 아직 없습니다. `/bid:design`으로 먼저 시작할까요?"*
2. **Outline loaded** — `proposal/.bidkit/meta/outline.yaml` must exist. If not, redirect to `/bid:design`.

---

## Dependency Check

When the user uploads an existing proposal as PPTX, DOCX, or XLSX:
1. Run `bash scripts/check-deps.sh`
2. If `bidkit-parser` is `false`, inform the user:
   "PPTX/DOCX 파일을 읽으려면 parser의 Python 의존성 설치가 필요합니다.
    터미널에서 실행: uv pip install -r parser/requirements.txt --system
    설치 후 다시 파일을 제공해주세요.
    PDF 형식이라면 바로 진단 가능합니다."
3. If `true`, parse and create SSOT files from extracted content.

## Entry Paths

`/diagnose` has two entry paths depending on whether the user uploads an existing proposal or works with the current project.

### Path A: Existing Proposal Uploaded

When the user uploads a document (PDF/DOCX/PPTX) alongside the `/diagnose` command:

1. **Parse document** — Extract content from the uploaded file, splitting into logical sections that map to the proposal outline.
2. **Create SSOT files** — For each identified section:
   - Create an SSOT file in `proposal/ssot/<team>/` using the `templates/ssot.md` template.
   - Set `status: existing` in front-matter.
   - Populate the body with the extracted content.
   - Map to the appropriate team (BA/DA/TA/SA) based on content analysis.
   - Set `dependencies` and `affects` based on cross-references found in the content.
3. **Update outline** — Populate `proposal/.bidkit/meta/outline.yaml` with the discovered sections if not already present.
4. **Fall through to Diagnosis** — proceed to the Diagnosis phase below.

### Path B: Current Project

When no document is uploaded and the project already has SSOTs:

1. **Read all SSOTs** — Load all SSOT files under `proposal/ssot/` and read both front-matter and body content.
2. **Read project metadata** — Load `proposal/.bidkit/meta/proposal-meta.yaml`, `proposal/.bidkit/meta/outline.yaml`, `proposal/.bidkit/meta/glossary.yaml`, and `proposal/.bidkit/meta/rfp-trace-matrix.md`.
3. **Proceed to Diagnosis** — continue to the Diagnosis phase below.

---

## Diagnosis Phase (Both Paths)

### Step (1) — Overseer Grades Each SSOT

The Overseer reads each SSOT and assigns a grade:

| Grade | Meaning | Criteria |
|-------|---------|----------|
| **A** | Excellent | Comprehensive coverage, accurate data, strong narrative, no gaps. Ready for final proposal. |
| **B** | Good | Solid content with minor issues. Needs light polish but no structural changes. |
| **C** | Needs work | Notable gaps, weak argumentation, missing data, or inconsistencies. Requires substantive revision. |
| **D** | Major issues | Fundamental problems — missing key requirements, wrong approach, inaccurate data. Needs major rewrite. |

For each SSOT, the Overseer records:
- Grade (A/B/C/D)
- 1-3 sentence rationale for the grade
- Specific issues found (categorized as Critical/Warning/Info)

### Step (2) — Per-Section Issue Identification

For each SSOT graded C or D, identify specific issues:

- **Content gaps** — RFP requirements not addressed, missing sections
- **Data issues** — inaccurate numbers, outdated specifications, missing sources
- **Argumentation weakness** — claims without evidence, weak competitive positioning
- **Structure problems** — poor organization, missing diagrams/tables, unclear flow
- **Quality shortfalls** — per `reference/quality-criteria.md` standards

### Step (3) — Cross-Cutting Verification

Analyze ALL SSOTs together across five dimensions. This replaces the former `/verify` command (now integrated into `/bid:diagnose`).

#### 3a. Terminology Consistency

Check all SSOTs for consistent use of terms against `proposal/.bidkit/meta/glossary.yaml`:

- **Server names** — the same server must be referred to by the same name everywhere
- **Product names** — exact product names, model numbers, and version strings must match
- **Abbreviations** — defined on first use and used consistently
- **Organization names** — customer, partner, vendor names identical everywhere
- **Technical terms** — match glossary definition

#### 3b. Data Accuracy

Check that numerical data is consistent across all SSOTs:

- **Server counts** — totals and per-type counts match between architecture and cost sections
- **Cost figures** — unit prices, totals, subtotals arithmetically correct and consistent
- **Performance metrics** — TPS, throughput, latency figures match between solution and architecture
- **Sizing data** — storage, memory, CPU specs match between solution specs and infra plans
- **Timeline data** — dates, durations, milestones consistent between implementation plan and overview
- **Licensing** — license counts match server/user counts in other sections

#### 3c. Redundancy Detection

- **Exact duplicates** — identical paragraphs or tables in multiple SSOTs
- **Near duplicates** — substantially similar content with minor variations (more dangerous as they may diverge)
- For each: determine if appropriate (e.g., executive summary) or should be consolidated

#### 3d. RFP Coverage Gap Analysis

- **Unmapped requirements** — requirements in `proposal/.bidkit/meta/rfp-trace-matrix.md` not assigned to any SSOT
- **Mapped but unaddressed** — assigned but not actually covered in content
- **Partial coverage** — mentioned but not elaborated
- **Orphan content** — content not mapping to any RFP requirement (scope creep)

#### 3e. Narrative Flow

- **Logical progression** — each section builds on the previous
- **Transitions** — sections reference or connect to adjacent sections
- **Consistency of tone** — writing style consistent across sections
- **Story arc** — clear beginning (problem), middle (solution), end (implementation + value)
- **Strategic coherence** — all sections support the same win strategy

#### Contract Validation (Optional)

If Node.js is available (`bash scripts/check-deps.sh` → `node: true`), run `scripts/validate-bidkit-contracts.js` for enhanced contract validation. If unavailable, skip with note: "고급 계약 검증이 생략되었습니다 (Node.js 미설치). 핵심 검증은 정상 수행됩니다."

### Step (4) — Diagnosis Report

Present the diagnosis report in two layers: **Decision List first** (what the user needs to decide), then **detailed report** (full breakdown).

```
## Diagnosis Report: [project name]

### 지금 결정할 것

1. [필수] sa-hsm-001 서버 수량을 12대와 14대 중 어떤 값으로 확정할지 결정
2. [필수] 제품 표준 명칭을 glossary 기준으로 통일 승인
3. [권장] ta-infra-001의 중복 사양표를 참조 방식으로 바꿀지 승인

### Overall Assessment
Grade distribution: A: N, B: N, C: N, D: N
Overall quality: [summary statement]

### Per-Section Grades (priority order — worst first)

#### [D] section-id: Section Title (team)
- Rationale: ...
- Issues:
  - [Critical] ...
  - [Warning] ...

#### [C] section-id: Section Title (team)
- Rationale: ...
- Issues:
  - [Critical] ...
  - [Warning] ...

#### [B] section-id: Section Title (team)
- Rationale: ...
- Issues:
  - [Info] ...

#### [A] section-id: Section Title (team)
- Rationale: ...

### Cross-Cutting Issues (priority order)

1. [Critical] Terminology: "보안 서버" vs "Security Server" — sa-hsm-001, ta-infra-001
2. [Critical] Data mismatch: server count 12 in sa-hsm-001 vs 14 in ba-cost-001
3. [Warning] Narrative gap: no transition between architecture and implementation plan
4. [Info] Redundancy: HSM specification duplicated in sa-hsm-001 and ta-infra-001

### Priority Improvement Order
1. section-id (D) — [reason this is highest priority]
2. section-id (C) — [reason]
3. Cross-cutting terminology fix — [reason]
...
```

---

## User Choice

After presenting the diagnosis report, offer the user four action paths:

### Option 1: Full Improvement

*"전체 개선을 진행합니다. 우선순위 순서대로 모든 섹션을 수정합니다."*

- Process all sections in the priority order determined by the diagnosis.
- Start with D-graded sections, then C, then B.
- Cross-cutting fixes are woven into each section as it is revised.

### Option 2: Selective Improvement

*"특정 섹션만 선택하여 개선합니다."*

- Present the priority list and let the user pick which sections to improve.
- User can select one or more sections by ID or number.
- Only selected sections go through the improvement loop.

### Option 3: Cross-Cutting Only

*"교차 문제부터 해결합니다 (용어, 데이터 일관성)."*

- Fix terminology inconsistencies across all SSOTs first.
- Fix data mismatches across all SSOTs.
- Update `proposal/.bidkit/meta/glossary.yaml` with resolved terms.
- Do not rewrite section content — only fix cross-cutting issues.

### Option 4: Re-prioritize

*"우선순위를 직접 설정합니다."*

- User specifies their own improvement order.
- Override the diagnosis-determined priority with user's preference.

---

## Sequential Improvement

For each selected SSOT (in priority order):

1. **Enter session loop** — invoke the `/bid:write` skill targeting the SSOT.
   - Mode is determined by the SSOT's current status per `/bid:write` state detection logic.
   - For `existing` status SSOTs: enters **Enhance** mode.
   - For `draft` or later status SSOTs: enters **Edit** or **Revise** mode as appropriate.
2. **Pass diagnosis context** — the `/bid:write` session receives:
   - The grade and rationale from the diagnosis.
   - The specific issues identified for this section.
   - Relevant cross-cutting problems that affect this section.
3. **Complete session loop** — each SSOT goes through the full `/bid:write` cycle (draft/revise, Critic verify, user approve, Overseer review).
4. **Progress tracking** — after each SSOT completes, show updated progress:
   ```
   Improvement Progress: 3/7 sections completed
   - [v] sa-hsm-001: D -> B (improved)
   - [v] ba-cost-001: C -> A (improved)
   - [v] ta-infra-001: C -> B (improved)
   - [~] da-model-001: C (in progress)
   - [ ] sa-impl-001: C (pending)
   - [ ] ba-req-001: B (pending)
   - [ ] ta-arch-001: B (pending)
   ```
5. **Move to next section** — after completing one SSOT, automatically transition to the next in priority order. Confirm with user: *"다음 섹션으로 넘어갑니다: [section]. 진행할까요?"*

---

## Final Integration Review

After all selected sections have been improved:

### Step (F1) — Before/After Comparison

For each improved section, present:

| Section | Before | After | Change |
|---------|--------|-------|--------|
| sa-hsm-001 | D | B | Major rewrite — added specifications, reference cases |
| ba-cost-001 | C | A | Data corrected, pricing model restructured |
| ... | ... | ... | ... |

### Step (F2) — Residual Issues

Identify any remaining issues that were not addressed:

- Issues deferred by user choice
- Issues blocked by missing dependencies
- Cross-cutting problems partially resolved
- Info-level items from Critic that were not addressed

### Step (F3) — Final Grading

Overseer re-grades all SSOTs (including those not selected for improvement) to produce the final assessment:

```
## Final Assessment: [project name]

### Grade Distribution
Before: A: 0, B: 2, C: 4, D: 1
After:  A: 3, B: 3, C: 1, D: 0

### Overall Quality Improvement
[summary of what changed and overall proposal readiness]

### Remaining Recommendations
- [section] — [what still needs attention]
```

### Step (F4) — Cross-Cutting Re-Check

Run a final cross-cutting consistency check (equivalent to the cross-cutting verification in `/bid:diagnose`) to ensure improvements did not introduce new inconsistencies.

---

## Error Handling

### No SSOTs to Diagnose

If no SSOT files exist and no document is uploaded:

```
진단할 내용이 없습니다. `/bid:design`으로 프로젝트를 먼저 만들거나, 기존 제안서를 업로드해 주세요.
```

### All SSOTs Grade A

If every section grades A:

```
모든 섹션이 우수합니다. 교차 검증만 수행합니다.
```

Then run cross-cutting checks only and present results.

### Document Parse Failure (Path A)

If the uploaded document cannot be parsed:

```
문서를 파싱할 수 없습니다. 지원 형식: PDF, DOCX, PPTX. 다른 형식으로 다시 업로드해 주세요.
```

---

## Key References

| File | Purpose |
|------|---------|
| `proposal/.bidkit/meta/outline.yaml` | Section ordering, team assignments, dependencies |
| `proposal/.bidkit/meta/proposal-meta.yaml` | Project name and metadata |
| `proposal/.bidkit/meta/glossary.yaml` | Term consistency reference |
| `proposal/.bidkit/meta/rfp-trace-matrix.md` | RFP requirement coverage |
| `proposal/ssot/<team>/<id>.md` | Per-section SSOT files |
| `reference/quality-criteria.md` | Domain-specific quality standards |
| `reference/proposal-guide-format.md` | Proposal Guide footer format |
| `reference/state-machine.md` | Valid SSOT states |
| `agents/overseer.md` | Overseer grading and cross-review protocol |
| `skills/write/SKILL.md` | Session loop for per-section improvement |

---

## Proposal Guide

**Render at the bottom of every response** per `reference/proposal-guide-format.md`.

Follows `reference/proposal-guide-format.md`.
