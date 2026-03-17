# /design — Proposal Strategy + TOC Setup

## Trigger

`/design` command or natural language like "RFP 받았는데 어디서부터?", "제안서 만들어야 해"

## User-Facing Goal

`/design` is the guided kickoff for a proposal project. The user should feel like
they are in a short strategy interview, not operating a multi-agent system.

Use situation-first wording such as:

- `전략 정리 중`
- `목차 확정 중`
- `섹션 방향 정리 중`

Avoid leading with internal role names unless needed for traceability.

## Hard Gate

Do not create SSOT files or start `/write` work until ALL of the following are approved:

1. Proposal strategy direction
2. Table of contents and team ownership
3. Initial section directions

If any of these are still unsettled, remain in `/design`.

## Conversation Rules

1. Ask **one focused question per turn**.
2. State **why the question matters** in one sentence.
3. Prefer **2-3 concrete options** with one recommended option first.
4. Summarize the current state at the top of each turn:
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

## Flow (Overseer-led)

1. **Accept input**: RFP upload, conversational context, existing proposal, or combination
2. **Context dialogue**: collect scope, competitors, strengths, constraints, timeline, stakeholders
3. **Strategy exploration**: present 2-3 strategic options with recommendation
4. **TOC co-design**: propose structure, assign teams, set priority order
5. **Section direction**: establish 1-2 sentence direction per section
6. **Project initialization**:
   - Create project directory: `proposal/` with subdirs `proposal/ssot/<team>/`, `proposal/.bidkit/meta/`, `proposal/.bidkit/runtime/`, `proposal/.bidkit/ideation/`, `proposal/output/`, `proposal/assets/`
   - Populate `proposal/.bidkit/meta/proposal-meta.yaml` from context
   - Populate `proposal/.bidkit/meta/outline.yaml` with TOC + SSOT ordering + priorities + `required_for_output` (always set explicitly; older projects that omit the field are treated as `true` — see `skills/output/SKILL.md`)
   - Populate `proposal/.bidkit/meta/glossary.yaml` with initial terms
   - Populate `proposal/.bidkit/meta/rfp-trace-matrix.md` if RFP provided
   - Populate `proposal/.bidkit/runtime/session-state.json` from `templates/init/runtime-state.json` — initialize `current_label` with the first user-facing situation label (e.g., "전략 정리 중"). Runtime state is optional helper state; if absent later, BidKit falls back to SSOT-derived status.
   - Create SSOT files (all in `ideation` state) with dependencies mapped
7. **Transition**: Show Proposal Guide recommending the first `/write` target

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
