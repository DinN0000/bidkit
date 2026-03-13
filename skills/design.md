# /design — Proposal Strategy + TOC Setup

## Trigger

`/design` command or natural language like "RFP 받았는데 어디서부터?", "제안서 만들어야 해"

## Flow (Overseer-led)

1. **Accept input**: RFP upload, conversational context, existing proposal, or combination
2. **Context dialogue**: Overseer asks about:
   - Project scope and customer
   - Competitors and their strengths
   - Our strengths and differentiators
   - Timeline and constraints
   - Key stakeholders
3. **Strategy exploration**: Present 2-3 strategic options with recommendations. Examples:
   - Cost leadership vs technology differentiation vs hybrid
   - Conservative vs aggressive scope
4. **TOC co-design**: Propose proposal structure based on strategy, user adjusts. Map sections to teams (BA/DA/TA/SA).
5. **Section direction**: Quick alignment on each section's direction (1-2 sentences each, not deep)
6. **Proposal brief generation**:
   - Create project directory: `meta/`, `ssot/<team>/`, `ideation/`, `assets/`
   - Populate `meta/proposal-meta.yaml` from context
   - Populate `meta/outline.yaml` with TOC + SSOT ordering + priorities
   - Populate `meta/glossary.yaml` with initial terms
   - Populate `meta/rfp-trace-matrix.md` if RFP provided
   - Create SSOT files (all in `ideation` state) with dependencies mapped
7. **Transition**: Show Proposal Guide recommending first `/write` target

## Input Sources (can combine)

- **RFP upload**: Parse PDF/DOCX, extract requirements, populate trace matrix
- **Conversational**: Ask questions to build context when no RFP
- **Existing proposal**: Load as baseline, create SSOTs with status `existing`

## Key Behaviors

- Always render Proposal Guide at bottom of every response
- Reference `agents/overseer.md` for Overseer behavior
- Reference `reference/proposal-guide-format.md` for guide rendering
- Reference `templates/init/` for template files
