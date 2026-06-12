# /design — Proposal Strategy + TOC Setup

## Trigger

`/design` command or natural language like "RFP 받았는데 어디서부터?", "제안서 만들어야 해",
"포트폴리오 만들어야 해", "사업 보고 써야 해", "경영 보고 준비해야 해"

## User-Facing Goal

`/design` is the guided kickoff for a persuasion-document project — every BidKit
document is a proposal: a proposer persuading an audience to make a decision.
The user should feel like they are in a short strategy interview, not operating
a multi-agent system.

## Step 0 — Doctype Determination (before everything else)

Determine the doctype FIRST — it governs inputs, team composition, checks, and
strategy frame for the rest of the flow (Key Rule 10).

1. Infer from the user's words: "제안서/RFP" → `proposal`, "포트폴리오/이력/지원" →
   `portfolio`, "보고/품의/검토/결재" → `business-report`.
2. If clear, confirm in one line and proceed: *"B2B 제안서로 진행합니다."*
3. If ambiguous, ask with ASCII previews (Key Rule 9):

```
어떤 제안을 준비하시나요?

[A] 제안서 (B2B)        [B] 포트폴리오          [C] 사업/경영 보고
 회사 ──→ 발주사         개인 ──→ 회사/클라이언트  팀 ──→ 의사결정자
 "우리를 선택하라"        "나를 선택하라"          "이 안을 승인하라"
 기준: RFP 요구사항       기준: JD·공고 역량       기준: 비용·효과·리스크
```

4. Load `reference/doctypes/<doctype>.md` and apply its profile to every
   subsequent step. Record `doctype` in `proposal/.bidkit/meta/proposal-meta.yaml`.

Use situation-first wording such as:

- `전략 정리 중`
- `목차 확정 중`
- `섹션 방향 정리 중`

Avoid leading with internal role names unless needed for traceability.

## Hard Gate

Do not create SSOT files or start `/bid:write` work until ALL of the following are approved:

1. Proposal strategy direction
2. Table of contents and team ownership
3. Initial section directions

If any of these are still unsettled, remain in `/bid:design`.

## Conversation Rules

1. Ask **one focused question per turn**.
2. State **why the question matters** in one sentence.
3. Prefer **2-3 concrete options** with one recommended option first.
4. **Show each option as a compact ASCII example** in a fenced code block whenever
   the choice has a visible shape — TOC options as outline trees, section structure
   options as heading/bullet skeletons, architecture directions as box diagrams.
   The user picks by comparing what the result looks like, not by reading prose
   descriptions (Key Rule 9).
5. Summarize the current state at the top of each turn:
   - `현재: 전략 정리 중`
   - `이번 단계: 경쟁 우위 방향 확정`
   - `질문: ...`

## Dependency Check

When the user provides a document file (PPTX, DOCX, XLSX) as RFP input:
1. Run `bash scripts/check-deps.sh`
2. If `bidkit-parser` is `false`, inform the user:
   "PPTX/DOCX 파일을 읽으려면 parser의 Python 의존성 설치가 필요합니다.
    터미널에서 실행: uv pip install -r parser/requirements.txt --system
    설치 후 다시 파일을 제공해주세요.
    PDF 형식의 RFP라면 바로 진행 가능합니다."
3. If `true`, parse the document using `from parser import parse` and proceed.

## Flow (Overseer-led, doctype profile applied)

1. **Accept input** (per doctype profile): proposal → RFP upload; portfolio →
   실적 자료 + 타깃 JD·공고; business-report → 보고 목적·결정 요청·근거 데이터.
   Existing documents and conversational context accepted for all doctypes.
2. **Context dialogue**: collect the persuasion frame — audience, decision
   requested, audience criteria, competitors/alternatives, strengths, constraints,
   timeline (questions adapt per doctype profile)
3. **Strategy exploration**: present 2-3 strategic options with recommendation,
   framed per doctype (win strategy / positioning / 권고안 채택 전략)
4. **TOC co-design**: propose structure, assign teams, set priority order
5. **Section direction**: establish 1-2 sentence direction per section
   - **MECE boundary**: for each section, also record `scope` (what it covers) and
     `not_in_scope` (adjacent topics with their owning section id). No two sections
     may claim the same content — shared data gets ONE owner; others reference it
     via `[REF: <ssot-id>]`. This is what prevents duplication downstream; resolve
     overlaps here, not after drafting.
6. **Project initialization**:
   - Create project directory: `proposal/` with subdirs `proposal/ssot/<team>/`, `proposal/.bidkit/meta/`, `proposal/.bidkit/runtime/`, `proposal/.bidkit/ideation/`, `proposal/output/`, `proposal/assets/`
   - Populate `proposal/.bidkit/meta/proposal-meta.yaml` from context — including
     `doctype`, `audience`, `decision_requested` (from Step 0 and context dialogue)
   - Populate `proposal/.bidkit/meta/outline.yaml` with TOC + SSOT ordering + priorities + `required_for_output` (always set explicitly; older projects that omit the field are treated as `true` — see `playbooks/output/SKILL.md`)
   - Populate `proposal/.bidkit/meta/glossary.yaml` with initial terms
   - Populate the criteria trace matrix per doctype profile: proposal →
     `rfp-trace-matrix.md` (if RFP provided); portfolio / business-report →
     `criteria-trace-matrix.md` (`templates/init/criteria-trace-matrix.md`)
   - Populate `proposal/.bidkit/runtime/session-state.json` from `templates/init/runtime-state.json` — initialize `current_label` with the first user-facing situation label (e.g., "전략 정리 중"). Runtime state is optional helper state; if absent later, BidKit falls back to SSOT-derived status.
   - Create SSOT files (all in `ideation` state) with dependencies and
     `scope` / `not_in_scope` boundaries mapped (from step 5)
7. **Transition**: Show Proposal Guide recommending the first `/bid:write` target

## Document Parsing

When the user provides an RFP document (PDF, DOCX, PPTX, XLSX):
- Parse the document using `parser/` module: `from parser import parse`
- Extract text, tables, and images into structured markdown
- Use extracted content to inform strategy and TOC generation
- Store raw parsed output in `proposal/assets/rfp/` for Researcher reference

## Input Sources (can combine)

- **RFP upload**: Parse PDF/DOCX, extract requirements, populate trace matrix
- **Conversational**: Ask guided questions when no RFP exists
- **Existing proposal**: Load as baseline, create SSOTs with status `existing`

## Key Behaviors

- Always render Proposal Guide at bottom of every response
- Always explain why the current question or option matters
- Prefer natural-language user guidance over command jargon
- Reference `agents/overseer.md` for Overseer behavior
- Reference `reference/proposal-guide-format.md` for guide rendering
- Reference `templates/init/` for template files
