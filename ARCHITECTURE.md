# Architecture

## System Topology

```
                    +-------------------------------+
                    |        Overseer (EA)          |
                    |  Strategy / Cross-SSOT review |
                    |       Final approval          |
                    +---+-------+-------+-------+---+
                        |       |       |       |
               +--------+  +---+---+  ++------++  +--------+
               |           |       |  |        |           |
          +----v----+ +----v----+ +v---v---+ +-v-------+
          | BA Team | | DA Team | | TA Team| | SA Team |
          | Lead    | | Lead    | | Lead   | | Lead    |
          | Writer  | | Writer  | | Writer | | Writer  |
          | Research| | Research| | Research| | Research|
          | Critic  | | Critic  | | Critic | | Critic  |
          |         | |         | |        | |         |
          | SSOT..  | | SSOT..  | | SSOT.. | | SSOT..  |
          +---------+ +---------+ +--------+ +---------+
```

Each team owns a set of SSOT documents. The Overseer coordinates across teams
and arbitrates conflicts. Teams work in parallel; only user-facing interactions
are sequential.

---

## Directory Map (BidKit Files)

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Codex BidKit entry point -- read first in Codex sessions |
| `CLAUDE.md` | Claude Code BidKit entry point -- same as `AGENTS.md` |
| `ARCHITECTURE.md` | This file -- system topology, file map, data flow |
| **`agents/`** | |
| `agents/overseer.md` | EA Overseer -- strategy, cross-review, conflict resolution |
| `agents/team-lead.md` | Team Lead -- per-domain orchestrator (parameterized by BA/DA/TA/SA) |
| `agents/writer.md` | Writer -- drafts and revises section content |
| `agents/researcher.md` | Researcher -- gathers specs, cases, certs, pricing |
| `agents/critic.md` | Critic -- independent quality verification |
| **`skills/`** | |
| `skills/design/SKILL.md` | `/design` -- new proposal strategy + TOC generation |
| `skills/write/SKILL.md` | `/write` -- session loop (draft/verify/revise), state auto-detected |
| `skills/diagnose/SKILL.md` | `/diagnose` -- quality diagnosis + cross-SSOT consistency check |
| `skills/status/SKILL.md` | `/status` -- progress dashboard + Proposal Guide renderer |
| `skills/output/SKILL.md` | Output assembly -- MD/PPT/PDF/HTML rendering |
| `skills/setup/SKILL.md` | Environment check and guided installation |
| **`templates/`** | |
| `templates/ssot.md` | SSOT document template (YAML frontmatter + body structure) |
| `templates/ideation-note.md` | Pre-SSOT exploration note template |
| `templates/init/proposal-meta.yaml` | Project metadata (customer, timeline, teams) |
| `templates/init/glossary.yaml` | Unified glossary template |
| `templates/init/outline.yaml` | TOC + SSOT ordering template |
| `templates/init/rfp-trace-matrix.md` | RFP requirements traceability template |
| `templates/init/runtime-state.json` | Runtime state template for current focus / next action |
| **`reference/`** | |
| `reference/state-machine.md` | SSOT lifecycle states and transition rules |
| `reference/quality-criteria.md` | Verification checklist per domain |
| `reference/proposal-guide-format.md` | Proposal Guide rendering spec (bottom of every response) |
| `reference/impact-rules.md` | Impact propagation severity rules (High/Medium/Low) |
| `reference/skills-catalog.md` | All agent skills mapped to roles |
| `reference/cross-team-communication.md` | Inter-team communication protocol |
| `reference/error-handling.md` | Error scenarios + graceful degradation |
| `reference/domain/ba.md` | BA domain structural patterns and Critic verification points |
| `reference/domain/da.md` | DA domain structural patterns and Critic verification points |
| `reference/domain/ta.md` | TA domain structural patterns and Critic verification points |
| `reference/domain/sa.md` | SA domain structural patterns and Critic verification points |
| **`parser/`** | |
| `parser/__init__.py` | Unified `parse()` entry point — auto-dispatches PDF vs Office |
| `parser/pdf_converter.py` | Docling-based PDF extraction (text, tables, images) |
| `parser/pdf_utils.py` | Bounding box helpers, figure category mapping |
| `parser/pdf_markdown.py` | PDF content → Markdown assembly |
| `parser/office_parser.py` | DOCX/PPTX/XLSX/RTF extraction via AST |
| `parser/office_types.py` | Office AST data structures and rendering |
| `parser/office_worker.py` | Batch processing worker |
| `parser/run.py` | CLI entry point for standalone parsing |
| `parser/requirements.txt` | Python dependencies (no AWS) |
| **`scripts/`** | |
| `scripts/verify-bidkit.sh` | BidKit integrity validation (file existence, cross-refs) |
| `scripts/validate-bidkit-contracts.js` | Contract validation for schema, output rules, and field naming (requires Node.js; skipped gracefully if unavailable) |
| `scripts/check-deps.sh` | Dependency detection (JSON output) |
| **`.claude-plugin/`** | |
| `.claude-plugin/plugin.json` | Plugin manifest (name: "bid") |
| **`evals/`** | |
| `evals/config.json` | Lightweight evaluation manifest for `/design`, `/write`, `/verify` |
| `evals/**` | Prompt and expected-output fixtures for regression checking |

---

## Project Directory (Created Per Proposal)

Created by `/design` at runtime. All proposal data lives under a single
`proposal/` root. User-facing content sits at the top level; internal data is
hidden in `.bidkit/`.

```
proposal/                        # Created by /design — all proposal data lives here
├── sections/                    # SSOT documents organized by team (user-facing)
│   ├── ba/*.md
│   ├── da/*.md
│   ├── ta/*.md
│   └── sa/*.md
├── output/                      # Generated deliverables (user-facing)
├── assets/                      # Diagrams, images, certificates (user-facing)
│   └── rfp/                     # Raw parsed RFP
└── .bidkit/                     # Internal data (hidden)
    ├── meta/                    # proposal-meta.yaml, outline.yaml, glossary.yaml, rfp-trace-matrix.md
    ├── runtime/                 # session-state.json (optional)
    └── ideation/                # Pre-SSOT exploration notes
```

| Path | Purpose |
|------|---------|
| **`proposal/ssot/<team>/`** | |
| `proposal/ssot/ba/*.md` | Business analysis SSOTs (overview, requirements, process) |
| `proposal/ssot/da/*.md` | Data architecture SSOTs (model, migration, security) |
| `proposal/ssot/ta/*.md` | Tech architecture SSOTs (architecture, implementation, cost) |
| `proposal/ssot/sa/*.md` | Solution/product SSOTs (HSM, DID, blockchain, etc.) |
| **`proposal/output/`** | Generated deliverables (proposal-vN.md, .pptx, .pdf, HTML site) |
| **`proposal/assets/`** | Diagrams (Mermaid source + rendered), images, certificates |
| `proposal/assets/rfp/` | Raw parsed RFP content |
| **`proposal/.bidkit/meta/`** | |
| `proposal/.bidkit/meta/proposal-meta.yaml` | Project info -- customer, project name, timeline, RFP reference |
| `proposal/.bidkit/meta/glossary.yaml` | Unified glossary -- terms, definitions, standard names |
| `proposal/.bidkit/meta/outline.yaml` | TOC -- section ordering, SSOT assignments, priority |
| `proposal/.bidkit/meta/rfp-trace-matrix.md` | RFP requirement ID -> mapped SSOT -> coverage status |
| **`proposal/.bidkit/runtime/`** | |
| `proposal/.bidkit/runtime/session-state.json` | Optional helper state: current situation label, active section, last completed step, recommended next action. This file is advisory — if missing or stale, BidKit falls back to SSOT-derived status. |
| **`proposal/.bidkit/ideation/`** | Pre-SSOT exploration notes (direction, alternatives, decisions) |

---

## Data Flow

```
User Input (RFP / conversation / existing proposal)
  |
  v
(1) Skill router ---- /design | /write | /diagnose | /verify | /status
  |
  v
(2) Overseer assigns teams, sets strategy
  |
  v
(3) Team Lead orchestrates per-section session loop:
      Researcher gathers data
        -> Writer drafts SSOT
          -> Critic verifies
            -> Writer revises (loop until pass)
  |
  v
(4) Runtime state (optional fallback) updates current user-facing situation and next action
  |
  v
(5) Team Lead presents to user -- user approves or requests changes
  |
  v
(6) Overseer cross-reviews confirmed SSOTs
      Pass -> status: confirmed
      Directive -> back to (3) for revision
  |
  v
(7) Output pipeline assembles confirmed SSOTs
      .bidkit/meta/outline.yaml -> ordering
      .bidkit/meta/glossary.yaml -> unified terms
      cross-references resolved
  |
  v
(8) Render to selected formats (MD always + PPT/PDF/HTML on request)
```

---

## Agent Interaction

**Within a team** (session loop):
- Team Lead receives work from Overseer or user command
- Team Lead directs Researcher to gather data
- Team Lead directs Writer to draft using research results
- Team Lead sends draft to Critic for independent verification
- Critic reports issues back to Team Lead (not Writer)
- Team Lead directs Writer + Researcher to revise
- Loop until Critic passes, then Team Lead presents to user

**Across teams** (Overseer-mediated):
- Dependency notification: Team Lead -> Team Lead when SSOT content changes
- Glossary sync: any Critic -> Overseer -> all teams
- Escalation: conflicting data between teams -> Overseer arbitrates
- Impact broadcast: re-edit of confirmed SSOT -> Overseer notifies affected teams

**Conflict resolution**:
1. Overseer detects contradiction (via `/verify` or automatic review)
2. Overseer identifies the authoritative source (SA owns product specs, TA owns infra)
3. Non-authoritative SSOT flagged for revision
4. Ambiguous authority -> Overseer asks user to decide
