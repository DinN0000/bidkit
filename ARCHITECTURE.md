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

## Directory Map (Harness Files)

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Codex harness entry point -- read first in Codex sessions |
| `CLAUDE.md` | Claude Code harness entry point -- same harness as `AGENTS.md` |
| `ARCHITECTURE.md` | This file -- system topology, file map, data flow |
| **`agents/`** | |
| `agents/overseer.md` | EA Overseer -- strategy, cross-review, conflict resolution |
| `agents/team-lead.md` | Team Lead -- per-domain orchestrator (parameterized by BA/DA/TA/SA) |
| `agents/writer.md` | Writer -- drafts and revises section content |
| `agents/researcher.md` | Researcher -- gathers specs, cases, certs, pricing |
| `agents/critic.md` | Critic -- independent quality verification |
| **`skills/`** | |
| `skills/design.md` | `/design` -- new proposal strategy + TOC generation |
| `skills/write.md` | `/write` -- session loop (draft/verify/revise), state auto-detected |
| `skills/diagnose.md` | `/diagnose` -- full quality diagnosis across all SSOTs |
| `skills/verify.md` | `/verify` -- cross-SSOT consistency and compliance check |
| `skills/status.md` | `/status` -- progress dashboard + Proposal Guide renderer |
| `skills/output.md` | Output assembly -- MD/PPT/PDF/HTML rendering |
| **`templates/`** | |
| `templates/ssot.md` | SSOT document template (YAML frontmatter + body structure) |
| `templates/ideation-note.md` | Pre-SSOT exploration note template |
| `templates/init/proposal-meta.yaml` | Project metadata (customer, timeline, teams) |
| `templates/init/glossary.yaml` | Unified glossary template |
| `templates/init/outline.yaml` | TOC + SSOT ordering template |
| `templates/init/rfp-trace-matrix.md` | RFP requirements traceability template |
| **`reference/`** | |
| `reference/state-machine.md` | SSOT lifecycle states and transition rules |
| `reference/quality-criteria.md` | Verification checklist per domain |
| `reference/proposal-guide-format.md` | Proposal Guide rendering spec (bottom of every response) |
| `reference/impact-rules.md` | Impact propagation severity rules (High/Medium/Low) |
| `reference/skills-catalog.md` | All agent skills mapped to roles |
| `reference/cross-team-communication.md` | Inter-team communication protocol |
| `reference/error-handling.md` | Error scenarios + graceful degradation |
| **`scripts/`** | |
| `scripts/verify-harness.sh` | Harness integrity validation (file existence, cross-refs) |

---

## Project Directory (Created Per Proposal)

Created by `/design` at runtime. Lives alongside or inside the harness directory.

| Path | Purpose |
|------|---------|
| **`meta/`** | |
| `meta/proposal-meta.yaml` | Project info -- customer, project name, timeline, RFP reference |
| `meta/glossary.yaml` | Unified glossary -- terms, definitions, standard names |
| `meta/outline.yaml` | TOC -- section ordering, SSOT assignments, priority |
| `meta/rfp-trace-matrix.md` | RFP requirement ID -> mapped SSOT -> coverage status |
| **`ssot/<team>/`** | |
| `ssot/ba/*.md` | Business analysis SSOTs (overview, requirements, process) |
| `ssot/da/*.md` | Data architecture SSOTs (model, migration, security) |
| `ssot/ta/*.md` | Tech architecture SSOTs (architecture, implementation, cost) |
| `ssot/sa/*.md` | Solution/product SSOTs (HSM, DID, blockchain, etc.) |
| **`ideation/`** | Pre-SSOT exploration notes (direction, alternatives, decisions) |
| **`assets/`** | Diagrams (Mermaid source + rendered), images, certificates |
| **`templates/`** | Company PPT master, PDF style, HTML theme |
| **`output/`** | Generated deliverables (proposal-vN.md, .pptx, .pdf, HTML site) |

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
(4) Team Lead presents to user -- user approves or requests changes
  |
  v
(5) Overseer cross-reviews confirmed SSOTs
      Pass -> status: confirmed
      Directive -> back to (3) for revision
  |
  v
(6) Output pipeline assembles confirmed SSOTs
      outline.yaml -> ordering
      glossary.yaml -> unified terms
      cross-references resolved
  |
  v
(7) Render to selected formats (MD always + PPT/PDF/HTML on request)
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
