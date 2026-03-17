# /output — Output Assembly and Format Rendering

## Trigger

Natural language: "PDF로 출력해줘", "PPT로 만들어줘", "최종본 출력", "이전 버전이랑 비교해줘"

---

## Dependency Check

When the user requests output in a specific format:
1. Run `bash scripts/check-deps.sh`
2. **PDF requested** and `pandoc` is `false`:
   "PDF 출력을 위해 pandoc이 필요합니다.
    설치: brew install pandoc (macOS) / apt install pandoc (Linux)
    Markdown 출력은 바로 가능합니다."
3. **PPTX requested** and `bidkit-parser` is `false`:
   "PPTX 출력을 위해 parser의 Python 의존성 설치가 필요합니다.
    터미널에서 실행: uv pip install -r parser/requirements.txt --system
    Markdown 출력은 바로 가능합니다."
4. If tools available, proceed with requested format.

## Assembly Engine Flow

When output is requested, execute the following steps in order:

### Step (1) — Load SSOT Ordering

Read `proposal/.bidkit/meta/outline.yaml` to determine the canonical section order and hierarchy. This is the single source of truth for document structure — do not reorder sections based on file system order or SSOT creation date.

### Step (2) — Collect Confirmed SSOTs

Scan `proposal/ssot/<team>/` for all SSOT files. Classify each by status:

| Status | Action |
|--------|--------|
| `confirmed` | Include in output |
| `tentative` | Include with `[TENTATIVE]` marker |
| `verified` | Include with `[PENDING OVERSEER REVIEW]` marker |
| `draft` / `verifying` | Exclude from output; log as missing |
| `ideation` / empty | Exclude from output; log as missing |
| `revision` | Exclude from output; log as blocked |

If a section in `proposal/.bidkit/meta/outline.yaml` does not specify `required_for_output`, it defaults to `true`. This ensures older or manually created outlines remain safe — no section is silently excluded from output gating.

If any sections with `required_for_output: true` (or defaulted to `true`) in `proposal/.bidkit/meta/outline.yaml` are missing or excluded, warn the user before proceeding:
*"[section-id] 섹션이 아직 확인되지 않았습니다. 제외하고 출력하시겠습니까?"*

### Step (3) — Generate Table of Contents

Build a TOC from `proposal/.bidkit/meta/outline.yaml` structure:
- Include section numbers, titles, and page anchors.
- Mark incomplete sections as `[미완성]` in the TOC.
- Depth: up to 3 levels (e.g., 1. / 1.1 / 1.1.1).

### Step (4) — Resolve Cross-References

Scan all collected SSOT content for cross-reference markers (e.g., `[REF: sa-hsm-001]`, `[SEE: ta-infra-001]`):
- Replace with the actual referenced content or a hyperlink in the target format.
- If the referenced SSOT is excluded (not confirmed), replace with `[참조 섹션 미완성 — <ssot-id>]`.
- Log all unresolved references for the user.

### Step (5) — Insert Glossary

Read `proposal/.bidkit/meta/glossary.yaml` and append a Glossary section at the end of the assembled document:
- Include all terms referenced in the collected SSOTs (match against each SSOT's `glossary_terms` metadata).
- Sort alphabetically.
- Format: term, definition, first used in section.

### Step (6) — Generate Unified Markdown

Always produce `proposal/output/proposal-vN.md` first, regardless of which formats the user requested:
- N is determined by reading existing files in `proposal/output/` and incrementing (e.g., `proposal-v3.md` if `proposal-v2.md` already exists).
- Structure: Cover page → TOC → Sections (in outline order) → Glossary → Appendices.
- Insert page-break markers (`---` or `<!-- page-break -->`) between major sections for downstream format renderers.
- Log: *"Markdown 생성 완료: proposal/output/proposal-vN.md"*

---

## Format Rendering

After `proposal/output/proposal-vN.md` is generated, render the user-requested format(s):

| Format | Characteristics |
|--------|----------------|
| Markdown | Always generated, editable source of truth |
| PPT | Company template mapping, slide layout per section |
| PDF | Page numbers, watermark, TOC auto-generation (`templates/pdf-style.css`) |
| HTML | Hyperlinks between sections, search, status badges (`templates/html-theme/`) |

> **Note — project-specific templates**: PPT rendering requires a company PPTX
> template (e.g., `templates/company-ppt.pptx`) that must be provided by the user
> during `/design` initialization. PDF and HTML templates ship with sensible
> defaults but can be customized per project.

### Output Paths

```
proposal/output/proposal-vN.md
proposal/output/proposal-vN.pptx
proposal/output/proposal-vN.pdf
proposal/output/proposal-vN/index.html     ← static site
```

### PPT Rendering

Source: Company PPTX template (provided during `/design` initialization)

Mapping rules:
- Each Level-1 section (`## `) -> new section divider slide.
- Each Level-2 section (`### `) -> content slide.
- Tables -> table slides (one table per slide; split if > 10 rows).
- Mermaid diagrams -> convert to image, insert as diagram slide.
- `## Summary` section -> speaker notes on the corresponding slide.
- TOC -> auto-generated TOC slide after cover.

### PDF Rendering

Source: `templates/pdf-style.css`

Features:
- Auto page numbers in footer (format: `[Project Name] — [Section] — p. N`).
- Watermark: `DRAFT` for tentative sections, `CONFIDENTIAL` on cover page.
- TOC with clickable page numbers.
- Section headers repeat on each page.

### HTML Rendering

Source: `templates/html-theme/`

Features:
- Hyperlinks between cross-referenced sections (resolved from step 4).
- Search bar (client-side, no server required).
- Status badges per section: `confirmed`, `tentative`, `pending`.
- Sidebar navigation from TOC.
- Output: static site at `proposal/output/proposal-vN/index.html`.

---

## Quick Edit Workflow

When the user requests a small change after output has been generated:

1. **Edit source SSOT** — apply the change to the relevant SSOT file.
2. **Impact check** — read the SSOT's `affects` metadata to identify downstream SSOTs.
3. **Cascade edits** — for each affected SSOT:
   - If the change is purely a reference update (e.g., a renamed term), auto-apply the cascade.
   - If the change affects content (e.g., a different product model), present each affected SSOT to the user and ask: *"[ssot-id]도 함께 수정할까요?"*
4. **Incremental rebuild**:
   - PPT: replace only the slides corresponding to changed sections.
   - PDF: full regeneration (page numbers may shift).
   - HTML: partial rebuild — only affected section pages regenerated.
   - Markdown: always full regeneration (fast).
5. Output paths retain the same version number N — overwrite in place.
6. Log: *"빠른 수정 완료. 영향 섹션: [list]. 재출력: proposal/output/proposal-vN.[ext]"*

---

## Version Diff

When the user asks to compare versions (e.g., "이전 버전이랑 비교해줘"):

1. **Identify versions** — list all `proposal/output/proposal-v*.md` files. Default: compare current (vN) vs. previous (vN-1). If the user specifies versions, use those.
2. **SSOT-level comparison** — for each SSOT present in either version, compare:
   - Content body (additions, deletions, modifications).
   - Status transitions (e.g., `draft` -> `confirmed`).
   - Version increment and history entries.
3. **Side-by-side diff output**:
   ```
   [섹션: sa-hsm-001 — HSM 솔루션]
   + 추가: ThalesGroup Luna Network HSM 7 사양 테이블 (3행)
   ~ 변경: 서버 수량 3대 -> 5대 (ta-infra-001 의존 업데이트 반영)
   - 삭제: 구형 Gemalto HSM 참조 제거
   이유: ta-infra-001 수정에 따른 연쇄 업데이트 (history: 2026-03-13)
   ```
4. **Change summary** — at the top of the diff, provide:
   - Total SSOTs changed / added / removed.
   - Sections promoted to `confirmed` since last version.
   - High-impact changes (sourced from history metadata).
5. **Output** — display diff inline. Optionally save to `proposal/output/diff-vN-vs-vN-1.md`.

---

## Executive Summary

When the user requests an executive summary (e.g., "요약본 만들어줘", "PM용 요약"):

1. Read all `confirmed` SSOTs and extract the body content under each `## Summary` section.
2. Compose a 1-page summary structured as:
   - **프로젝트 개요** (2-3 sentences from `proposal/.bidkit/meta/proposal-meta.yaml`)
   - **핵심 제안 내용** (1 bullet per confirmed section, drawn from each SSOT's `## Summary`)
   - **주요 수치** (key numbers: cost, timeline, headcount, performance targets)
   - **미결 사항** (sections not yet confirmed, with expected completion)
3. Output: `proposal/output/executive-summary-vN.md`.
4. If PPT was also requested, generate as a single slide (`proposal/output/executive-summary-vN.pptx`).

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
6. Output generated, small change needed -> natural language quick edit guidance
7. Versions available -> `/output diff` to compare versions
