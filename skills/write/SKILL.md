# /write — Session Loop for SSOT Content

## Trigger

`/write <section>` command or natural language like "HSM 모델 변경해야 해", "이행계획 어떻게 할지 고민 중이야", "보안 아키텍처 써줘", "sa-hsm-001 수정하자"

The `<section>` argument accepts any of the following forms:
- SSOT ID: `sa-hsm-001`
- Section title: `HSM 솔루션`
- Keyword match: `hsm`, `이행`, `보안`
- Outline position: `3.2.1`

If ambiguous, list matching SSOTs and ask the user to pick one.

## User-Facing Mode Labels

Lead with the user-facing situation label instead of the raw state name:

| Internal Mode | User-Facing Label |
|---------------|-------------------|
| Create | 새로 작성 중 |
| Explore | 방향 탐색 중 |
| Edit | 초안 보완 중 |
| Revise | 수정 반영 중 |
| Re-edit | 확정본 수정 검토 중 |
| Enhance | 기존안 보강 중 |
| Directive | 최종 검토 지시 반영 중 |

---

## Dependency Check

When source documents (RFP, prior proposals, reference materials) are PPTX, DOCX, or XLSX:
1. Run `bash scripts/check-deps.sh`
2. If `bidkit-parser` is `false`, inform the user:
   "PPTX/DOCX 파일을 읽으려면 parser의 Python 의존성 설치가 필요합니다.
    터미널에서 실행: uv pip install -r parser/requirements.txt --system
    설치 후 다시 시도해주세요."
3. If `true`, parse and provide to Researcher as structured input.

## Prerequisites

Before entering the session loop, verify:

1. **Project exists** — `proposal/.bidkit/meta/proposal-meta.yaml` must exist. If not, redirect: *"프로젝트가 아직 없습니다. `/design`으로 먼저 시작할까요?"*
2. **SSOT exists** — the target SSOT file must exist under `proposal/ssot/<team>/`. If not found in `proposal/.bidkit/meta/outline.yaml` either, redirect to `/design` to add the section.
3. **Outline loaded** — read `proposal/.bidkit/meta/outline.yaml` for section ordering and dependencies.
4. **Glossary loaded** — read `proposal/.bidkit/meta/glossary.yaml` for term consistency.
5. **RFP trace matrix loaded** — read `proposal/.bidkit/meta/rfp-trace-matrix.md` for requirement mapping to this section.
6. **Runtime state loaded if present** (advisory only) — read `proposal/.bidkit/runtime/session-state.json` for the last active section and current user-facing stage. Runtime state is advisory only: it may be missing or stale. Always use SSOT front-matter as the authoritative source for section status. If runtime state conflicts with SSOT metadata, prefer the SSOT.

---

## State Detection Logic

On invocation, read the target SSOT front-matter `status` field and auto-detect mode. **Never ask the user which mode to use** — detect it.

| SSOT State | Mode | Entry Point | Behavior |
|------------|------|-------------|----------|
| Empty / `ideation` (with direction) | **Create** | Full session loop from step (1) | Fresh content creation. Full context gathering, research, drafting, verification cycle. |
| `ideation` (empty direction) | **Explore** | Auto-enter Explore mode first | No direction established yet. Conduct exploratory dialogue before writing. |
| `draft` | **Edit** | Session loop from step (6) | Content exists but has not passed verification. Direct Writer to revise, then Critic to verify. |
| `verified` / `tentative` | **Revise** | Session loop from step (6) | Content was verified or user-approved. Direct Writer to incorporate requested changes, then Critic must re-verify from scratch. |
| `confirmed` | **Re-edit** | Warning + impact analysis, then step (6) | Content was Overseer-approved. Show impact warning, perform cascade analysis per `reference/impact-rules.md`, then proceed to revision. |
| `existing` | **Enhance** | Session loop from step (5) | Imported from prior proposal. Existing content serves as starting draft. Send directly to Critic for gap analysis, then revise. |
| `revision` | **Directive** | Session loop from step (6) | Overseer issued a directive. Parse directive from `verification.overseer_directive`, address specific issues. |

### Mode Announcement

At session start, announce the detected mode to the user:

- **Create**: *"현재: 새로 작성 중. 이번 단계에서 [section] 초안을 시작합니다."*
- **Explore**: *"현재: 방향 탐색 중. [section]은 아직 방향이 정해지지 않았습니다."*
- **Edit**: *"현재: 초안 보완 중. 검증 피드백을 반영해 [section]을 다듬습니다."*
- **Revise**: *"현재: 수정 반영 중. [section]은 재검증이 필요한 상태입니다."*
- **Re-edit**: *"현재: 확정본 수정 검토 중. [section] 수정 시 연관 섹션에 영향이 있을 수 있습니다."*
- **Enhance**: *"현재: 기존안 보강 중. 기존 제안서 내용을 기준으로 [section]을 강화합니다."*
- **Directive**: *"현재: 최종 검토 지시 반영 중. Overseer 지시사항을 [section]에 반영합니다."*

---

## Explore Mode (auto-triggered when direction is empty)

When `/write` targets a section with no established direction (empty SSOT or `ideation` state with `ideation.direction: null`), auto-enter Explore mode before the session loop.

### Explore Flow

#### (E1) Team Lead Opens Exploration

- Read related SSOTs and project context from `proposal/.bidkit/meta/proposal-meta.yaml`.
- Identify what this section needs to cover based on `proposal/.bidkit/meta/outline.yaml` and `proposal/.bidkit/meta/rfp-trace-matrix.md`.
- Ask the user exactly one structured question per turn, and explain why it matters:
  *"HSM 방식은 크게 두 가지입니다: (A) 네트워크 HSM (추천) — 중앙 관리 용이, (B) PCIe HSM — 지연시간 최소화. 어떤 방향이 맞을까요?"*

#### (E2) Researcher Gathers Background

- Team Lead directs Researcher to collect:
  - RFP requirements relevant to this section
  - Competitor approaches and market trends
  - Reference cases from similar projects
  - Regulatory requirements and compliance mandates
  - Product options and pricing ranges

#### (E3) Present Options with Trade-offs

For each viable direction, present:

| Aspect | Option A | Option B | Option C (if applicable) |
|--------|----------|----------|--------------------------|
| Summary | ... | ... | ... |
| Pros | ... | ... | ... |
| Cons | ... | ... | ... |
| Risk | ... | ... | ... |
| Effort | ... | ... | ... |
| RFP fit | ... | ... | ... |

Include a clear recommendation with rationale.

#### (E4) Iterate Until Direction Confirmed

- If the user picks an option -> proceed.
- If the user asks for more detail on an option -> Researcher dives deeper, present refined analysis.
- If the user proposes a new direction -> evaluate feasibility, add to options.
- If the user is undecided -> narrow down by asking more focused questions.

#### (E5) Save Ideation Notes

Once direction is confirmed:
1. Update the SSOT `ideation.direction` field with the confirmed direction.
2. Update `ideation.alternatives_considered` with rejected options and rationale.
3. Update `ideation.notes` with key decisions and constraints.
4. Set SSOT status to `ideation` (if not already).
5. Save an ideation note file to `proposal/.bidkit/ideation/<ssot-id>.md` using the `templates/ideation-note.md` template.

#### (E6) Transition to Create Mode

Ask: *"방향이 정해졌습니다. 바로 작성을 시작할까요?"*
- **Yes** -> Transition to Create mode, begin session loop at step (1).
- **Not now** -> Save state, show Proposal Guide with recommendation to return.

---

## Session Loop (10 Steps)

### Team Lead Phase

#### Step (1) — Context Gathering

**Owner**: Team Lead
**Applies to**: Create mode (all other modes skip to their entry point)

1. **Read SSOT metadata**: Load front-matter — check `status`, `dependencies`, `affects`, `ideation`, `history`, `version`.
2. **Check dependencies**: For each SSOT in `dependencies`, read its current state and key content:
   - If dependency is `confirmed` -> use its data as authoritative.
   - If dependency is `draft` or later -> use its data but flag as potentially changing.
   - If dependency is `ideation` or empty -> note as `[PENDING]` placeholder.
3. **Check RFP mapping**: Read `proposal/.bidkit/meta/rfp-trace-matrix.md` to identify which RFP requirements this section must address. List them explicitly.
4. **Check glossary**: Read `proposal/.bidkit/meta/glossary.yaml` for terms relevant to this section's domain.
5. **Ask user questions** with recommended options:
   - Ask one question first. Ask a second only if the first answer creates a new blocker.
   - Questions must be specific to this section, not generic.
   - Always offer concrete choices and why they matter: *"서버 이중화 방식은 비용과 가용성을 결정합니다. (A) Active-Standby (추천 — 비용 효율), (B) Active-Active (고가용성 우선). 어떤 방식으로 할까요?"*
   - If the ideation notes contain enough direction, skip questions and summarize the plan instead: *"탐색 단계에서 [방향]으로 결정되었습니다. 이 방향으로 진행하겠습니다."*

#### Step (2) — Direct Researcher

**Owner**: Team Lead
**Applies to**: Create mode

When source documents (RFP, prior proposals, reference materials) are provided:
- Parse using `parser/` module for structured extraction
- Researcher uses parsed output as primary source material
- Extracted tables and images are available in `proposal/assets/` directory

Issue a structured research directive to the Researcher. The directive must specify:

- **What to gather**: Specific data points needed for this section.
  - Product specifications (model names, versions, TPS, certifications)
  - Reference cases (similar deployments, customer names, outcomes)
  - Pricing data (list prices, license models, maintenance costs)
  - Regulatory requirements (applicable guidelines, clause references)
  - Competitor data (alternative products, competitive positioning)
- **Where to look**: Uploaded documents, prior proposals, external references, RFP appendices.
- **Return format**: Structured findings with confidence levels per `agents/researcher.md` output format.
- **Priority items**: Which data points are critical (blocking the draft) vs. nice-to-have.

---

### Parallel Work Phase

#### Step (3) — Researcher Gathers Data

**Owner**: Researcher
**Applies to**: Create mode

The Researcher executes the directive from step (2):
- Gathers specifications, reference cases, certifications, pricing, regulatory data.
- Structures findings with source attribution and confidence levels (High / Medium / Low).
- Identifies gaps — data that could not be found — with suggestions for where to obtain it.
- Returns results in the structured format defined in `agents/researcher.md`.

#### Step (4) — Writer Drafts Content

**Owner**: Writer
**Applies to**: Create mode

The Writer produces a complete SSOT body using:
- **Researcher's structured output** as the data foundation.
- **Team Lead's direction** from step (1) as the strategic frame.
- **SSOT template** (`templates/ssot.md`) as the structural guide.
- **Quality criteria** (`reference/quality-criteria.md`) as the quality target.

The draft must include:

| Section | Content |
|---------|---------|
| **Summary** | 3-5 sentence executive overview with key numbers and strategic positioning |
| **Content** | Main body organized by logical sub-sections with headings, tables, and diagrams |
| **Supporting Evidence** | Reference cases, benchmarks, certifications from Researcher output |

**Diagram and table requirements**:
- At least one Mermaid diagram per major architectural or process concept.
- Specification tables for product details, pricing, or comparisons.
- All diagrams and tables must have descriptive titles and captions.
- Use Korean labels when content is in Korean.

**SSOT metadata updates during drafting**:
- Set `status: draft` (transition from `ideation`).
- Increment `version` if revising an existing draft.
- Append to `history`: `{ step: "draft", timestamp: <now>, summary: "<what was done>" }`.
- Update `skills_used` with any skills employed (Mermaid, FP estimation, etc.).
- Update `diagrams` with list of diagrams generated.

---

### Verification Phase

#### Step (5) — Critic Verifies

**Owner**: Critic
**Applies to**: Create mode (first verification), Enhance mode (entry point)

The Critic performs independent verification against the full checklist defined in `agents/critic.md`:

1. **RFP requirements coverage** — every mapped requirement addressed?
2. **Data accuracy** — numbers, model names, specs match Researcher sources?
3. **Gap analysis** — any sections lacking sufficient detail?
4. **Cross-SSOT consistency** — values match dependency SSOTs?
5. **Glossary compliance** — terms consistent with `proposal/.bidkit/meta/glossary.yaml`?
6. **Regulatory compliance** — applicable regulations addressed?

**Output**: Structured verification report with:
- Verdict: PASS or FAIL
- Issues categorized: Critical / Warning / Info
- Each issue with: description, location, evidence, suggested fix
- Summary: checks performed, issue counts, verdict rationale

**State transition**:
- On verification start: `status: verifying`
- Update `verification.checklist_passed` with pass ratio
- Update `verification.critic_issues` with issue list

#### Step (6) — Writer + Researcher Revise

**Owner**: Writer and Researcher (parallel)
**Applies to**: All modes except Create (which enters here after step 5 FAIL)

When the Critic fails the draft (or the user/Overseer requests changes):

**Writer**:
- Receives Critic's issue list via Team Lead, filtered by priority.
- Addresses all Critical issues (mandatory).
- Addresses all Warning issues (mandatory).
- Addresses Info issues where feasible.
- Does NOT alter content that was not flagged unless directly related to a flagged issue.

**Researcher** (parallel, when needed):
- Gathers additional data for gaps identified by the Critic.
- Verifies or corrects specific claims flagged as inaccurate.
- Supplies missing reference cases or benchmarks.

**SSOT metadata updates**:
- Set `status: draft` (transition from `verifying` on fail).
- Increment `version`.
- Append to `history`: `{ step: "revision", timestamp: <now>, summary: "<issues addressed>" }`.

#### Step (7) — Critic Re-Verifies

**Owner**: Critic
**Applies to**: After every step (6) revision

The Critic re-verifies the revised content:

1. Confirm all prior Critical and Warning issues are resolved.
2. Check that revisions did not introduce new issues.
3. Verify any new data added by the Researcher.
4. Produce an updated verification report with resolution status for prior issues.

**Verdict rules**:
- Zero Critical + Zero Warning -> **PASS** -> proceed to step (8).
- Any Critical or Warning remaining -> **FAIL** -> return to step (6).
- Only Info issues -> **PASS** (Info items noted for optional improvement).

**Loop guard**: If the Critic fails the draft on the same issue more than twice:
- Team Lead escalates to the user for guidance.
- Do not loop indefinitely — present the issue and ask for a decision.

**State transition on PASS**:
- `status: verified`
- `verification.checklist_passed` updated to reflect pass

---

### User Phase

#### Step (8) — Team Lead Presents to User

**Owner**: Team Lead
**Applies to**: After Critic passes (step 7 PASS)

Present the completed work to the user with the following structure:

**a) Summary of What Was Written**
- 3-5 sentence overview of the section content.
- What data sources were used.
- What RFP requirements are addressed.

**b) Key Decisions Made**
- Decisions made during drafting that the user should be aware of.
- Why each decision was made (rationale from research or strategic direction).
- Flag any decisions that were made with Low-confidence data.

**c) Recommendation + Alternatives**
- The recommended approach (already in the draft) with rationale.
- At least one alternative approach that was considered.
- Why the recommendation is preferred over alternatives.

**d) Content Preview**
- Full SSOT content for user review.
- Highlight sections that depend on pending data (`[PENDING]` markers).
- Note any Critic Info items that were not addressed.

**e) User Options**
Present clear action choices in user language:
- **Approve** -> proceed to step (9)
- **Request changes** -> describe what to change, return to step (6) with specific revision instructions
- **Change direction** -> fundamental rethink, return to step (4) with new direction
- **Pause** -> save current state, return later

#### Step (9) — Tentative Confirmation

**Owner**: Team Lead
**Applies to**: After user approves in step (8)

1. Record user approval: set `verification.user_approved: true`.
2. Transition SSOT state: `status: tentative`.
3. Increment `version`.
4. Append to `history`: `{ step: "user_approved", timestamp: <now>, summary: "User approved" }`.
5. Report to Overseer with:
   - SSOT ID and current state
   - Content summary
   - Known cross-team dependencies or potential conflicts
   - Any new glossary terms introduced or modified
6. Inform user: *"[section]이 잠정 확인되었습니다. Overseer 검토를 진행합니다."*

---

### Overseer Phase

#### Step (10) — Overseer Cross-Review

**Owner**: Overseer
**Applies to**: After step (9) — mandatory AND automatic (triggered when SSOT reaches `tentative`; no user command needed)

The Overseer performs a mandatory cross-review per `agents/overseer.md`:

1. **Terminology consistency** — all terms match `proposal/.bidkit/meta/glossary.yaml`.
2. **Numeric consistency** — server counts, costs, throughput match across all related SSOTs.
3. **Name consistency** — product names, server names identical everywhere.
4. **Strategic alignment** — content supports agreed strategy.
5. **RFP coverage** — all mapped requirements addressed.
6. **Regulatory compliance** — applicable regulations satisfied.
7. **Quality criteria** — domain-specific quality standards met.

**Verdict**:
- **Pass** -> `status: confirmed`. Set `verification.overseer_approved: true`. Notify Team Lead: *"[section] — Overseer 승인 완료."*
- **Issue directive** -> `status: revision`. Set `verification.overseer_directive` with specific issues. Notify Team Lead with actionable changes. Return to step (6).

**SSOT metadata updates**:
- Append to `history`: `{ step: "overseer_review", timestamp: <now>, summary: "<verdict + details>" }`.
- Update Overseer Review Log table in the SSOT body.

---

## Re-edit Impact Analysis (for `confirmed` SSOTs)

When `/write` targets a `confirmed` SSOT, perform impact analysis before any changes:

### Impact Analysis Flow

1. **Show warning**: *"⚠ 이 섹션은 최종 확인된 상태입니다. 수정하면 연관 섹션에 영향이 있을 수 있습니다."*

2. **Read `affects` metadata**: List all downstream SSOTs that depend on this SSOT's content.

3. **Classify change severity** per `reference/impact-rules.md`:

   | Severity | Criteria | Action |
   |----------|----------|--------|
   | **High** | Primary data point consumed by affected SSOTs (product model, quantity, price, architecture component) | Force re-verify all affected SSOTs |
   | **Medium** | Referenced but not structurally critical (hostname, label, descriptive text) | Notify user, let them decide which SSOTs to re-verify |
   | **Low** | Purely cosmetic or prose-only, no cross-SSOT reference | Log the change only |

4. **Build dependency graph**: Check for transitive dependencies. If SSOT-A affects SSOT-B which affects SSOT-C, show the full cascade.

5. **Present impact summary to user**:
   ```
   영향 분석:
   - [High] sa-hsm-001 -> ta-infra-001 (서버 수량 참조)
   - [High] sa-hsm-001 -> ba-cost-001 (가격 정보 참조)
   - [Medium] sa-hsm-001 -> da-model-001 (데이터 모델 참조)
   총 영향 SSOT: 3개 (High: 2, Medium: 1)
   ```

6. **Require user confirmation**: *"계속 진행하시겠습니까?"*
   - **Yes** -> proceed to step (6) with the SSOT in `revision` state.
   - **No** -> abort, no changes made.

7. **Cascade threshold**: If more than 5 SSOTs are affected, require explicit confirmation: *"5개 이상의 섹션에 영향이 있습니다. 정말 진행하시겠습니까?"*

---

## SSOT Lifecycle Management

Every `/write` session must maintain SSOT metadata integrity:

### Version Management

- Increment `version` on each substantive revision (draft, revision, user approval).
- Never decrement versions.

### Status Transitions

Only valid transitions per `reference/state-machine.md`:

```
ideation -> draft -> verifying -> verified -> tentative -> reviewing -> confirmed
                        |                                      |
                        +-- fail --> draft                     +-- directive --> revision -> verifying
```

### History Tracking

Append to the `history` array on every state transition:

```yaml
history:
  - step: "draft"
    timestamp: "2026-03-13T10:00:00"
    summary: "Initial draft created based on RFP requirements"
  - step: "verification"
    timestamp: "2026-03-13T10:30:00"
    summary: "Critic found 2 Critical, 1 Warning issues"
  - step: "revision"
    timestamp: "2026-03-13T11:00:00"
    summary: "Addressed C-001 (model name), C-002 (pricing), W-001 (certification)"
  - step: "verified"
    timestamp: "2026-03-13T11:30:00"
    summary: "All issues resolved, Critic passed"
  - step: "user_approved"
    timestamp: "2026-03-13T12:00:00"
    summary: "User approved with no changes"
  - step: "overseer_review"
    timestamp: "2026-03-13T14:00:00"
    summary: "Overseer approved, confirmed"
```

### Glossary Updates

When the Writer introduces new technical terms:
1. Check if the term exists in `proposal/.bidkit/meta/glossary.yaml`.
2. If new, propose the term to the Overseer for approval.
3. Once approved, add to `proposal/.bidkit/meta/glossary.yaml` and update the SSOT's `glossary_terms` list.
4. Broadcast the new term to all Team Leads per `reference/cross-team-communication.md`.

### Outline Updates

If the session results in a new section being added or an existing section being moved:
1. Update `proposal/.bidkit/meta/outline.yaml` with the new structure.
2. Verify that section ordering and dependencies remain consistent.

---

## Auto-Split Rule

When SSOT content meets either threshold, propose splitting to the user:
- Content exceeds approximately **30 pages** (estimated from section length).
- Content contains **3 or more independently verifiable sub-items**.

### Split Process

1. Identify logical split boundaries.
2. Propose the split with clear descriptions of each child SSOT.
3. Wait for user approval.
4. On approval:
   - Create child SSOT files with `parent` metadata linking to the original.
   - Inherit `dependencies` and `affects` relationships where applicable.
   - Each child starts at `ideation` or `draft` depending on content maturity.
5. Update the parent SSOT to reference its children.
6. Update `proposal/.bidkit/meta/outline.yaml` with the new structure.

---

## Error Recovery

### Dependency SSOT Not Ready

When a dependency SSOT has not been drafted yet:
- Use placeholder: `[PENDING: <ssot-id> — <what is needed>]`
- Flag the placeholder in the verification report.
- Continue with the draft — do not block on missing dependencies.
- When the dependency is later completed, the placeholder must be replaced and the section re-verified.

### Session Interrupted

SSOT files on disk are the persistence layer:
- On next session start, read all SSOT front-matter to reconstruct state.
- Resume from the last completed step.
- The Proposal Guide reflects current state automatically.

### Critic Loop Guard

If the Critic fails the same issue more than twice:
- Team Lead escalates to the user.
- Present the issue with both the Critic's concern and the Writer's response.
- Ask the user to decide: fix, override (with documented rationale), or defer.

### Unfixable Issues

When the Writer cannot resolve an issue without external input:
- Escalate to the user via the Team Lead.
- Mark the SSOT as `draft` with a blocker note.
- Do not block other SSOTs — continue work on independent sections.

---

## Agent Coordination Summary

| Step | Owner | Input | Output | Next |
|------|-------|-------|--------|------|
| (1) Context gathering | Team Lead | SSOT metadata, dependencies, RFP trace | Context summary, user questions | (2) |
| (2) Direct Researcher | Team Lead | Context from (1), user answers | Research directive | (3) |
| (3) Researcher gathers | Researcher | Directive from (2) | Structured research results | (4) |
| (4) Writer drafts | Writer | Research from (3), direction from (1) | Complete SSOT draft | (5) |
| (5) Critic verifies | Critic | Draft from (4) | Verification report (PASS/FAIL) | (6) or (8) |
| (6) Writer + Researcher revise | Writer, Researcher | Critic issues from (5)/(7) | Revised SSOT | (7) |
| (7) Critic re-verifies | Critic | Revised draft from (6) | Updated verification report | (6) or (8) |
| (8) Present to user | Team Lead | Verified SSOT | Summary + content preview | (9) or (6) or (4) |
| (9) Tentative confirmation | Team Lead | User approval | SSOT status: tentative | (10) |
| (10) Overseer cross-review | Overseer | Tentative SSOT | Verdict: confirmed or directive | Done or (6) |

---

## Key References

| File | Purpose |
|------|---------|
| `reference/state-machine.md` | Valid SSOT state transitions |
| `reference/impact-rules.md` | Re-edit severity and cascade rules |
| `reference/proposal-guide-format.md` | Proposal Guide rendering at bottom of every response |
| `reference/quality-criteria.md` | Domain-specific quality standards for verification |
| `reference/cross-team-communication.md` | Inter-team notification protocol |
| `reference/error-handling.md` | Error recovery procedures |
| `agents/team-lead.md` | Team Lead orchestration behavior |
| `agents/writer.md` | Writer drafting and revision rules |
| `agents/researcher.md` | Researcher data gathering format |
| `agents/critic.md` | Critic verification checklist and output format |
| `agents/overseer.md` | Overseer cross-review protocol |
| `templates/ssot.md` | SSOT document structure |
| `templates/ideation-note.md` | Ideation note template for Explore mode |

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
