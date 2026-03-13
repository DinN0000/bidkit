# /status — Progress Dashboard

## Trigger

`/status` command or natural language like "진행 상황 알려줘", "어디까지 했어?", "현재 상태 보여줘", "뭐가 확인됐어?"

---

## Prerequisites

1. **Project exists** — `meta/proposal-meta.yaml` must exist. If not, redirect: *"프로젝트가 아직 없습니다. `/design`으로 먼저 시작할까요?"*
2. **Outline loaded** — `meta/outline.yaml` must exist. If not, redirect to `/design`.

---

## Flow

### Step (1) — Read All State Files

Load the following files in parallel:

1. **`meta/outline.yaml`** — section ordering, team assignments, dependencies.
2. **`meta/proposal-meta.yaml`** — project name, RFP reference, team composition.
3. **All SSOT files under `ssot/`** — read front-matter (`status`, `version`, `verification`, `dependencies`, `ideation`) for each file. Do not read full body content — only front-matter metadata is needed for the dashboard.

### Step (2) — Compute Per-Section Status

For each section in `meta/outline.yaml` order:

- Map to its SSOT file (if it exists) and read its `status` field.
- If no SSOT file exists yet: `not_started`.
- If SSOT exists but `status` is absent: `not_started`.
- Classify into dashboard bucket:

| SSOT status field | Dashboard bucket | Icon |
|---|---|---|
| `confirmed` | Confirmed | `[v]` |
| `draft`, `verifying`, `verified`, `tentative`, `reviewing` | In Progress | `[~]` |
| `ideation` | Ideation | `[>]` |
| `revision` | Revision (Overseer directive) | `[!]` |
| absent / `not_started` | Not Started | `[ ]` |

- For `[~]` items: note the current sub-status (e.g., "Critic reviewing", "verifying").
- For `[!]` items: extract `verification.overseer_directive` summary and include it.
- For `[>]` items: check `ideation.direction` — if populated, note the direction; if null, mark as "방향 미정".

### Step (3) — Identify Blocked Items

For each SSOT with `dependencies` listed in front-matter:

- Check whether each listed dependency SSOT has `status: confirmed`.
- If any dependency is NOT confirmed: mark the SSOT as **Blocked**.
- Blocked items can still be in progress — being blocked means full confirmation is gated.

### Step (4) — Compute Overall Progress

```
confirmed_count = count of SSOTs with status: confirmed
total_count     = total SSOT count defined in meta/outline.yaml
percentage      = round(confirmed_count / total_count * 100)
```

### Step (5) — Group by Team

Group sections by their team assignment from `meta/outline.yaml`:

- **BA** — Business Analysis team
- **DA** — Data Architecture team
- **TA** — Technical Architecture team
- **SA** — Solution Architecture team

Within each team, list sections in outline order.

### Step (6) — Determine Active Work

Active items are SSOTs with `status` in: `draft`, `verifying`, `verified`, `tentative`, `reviewing`, `revision`.

For each active SSOT, show:
- Current status
- Last `history` entry summary (most recent activity)

### Step (7) — Determine Next Priority

Use the same Recommendation Logic as the Proposal Guide:

1. All SSOTs empty or not started -> recommend `/write <first priority section>`
2. Some sections in draft/verifying -> recommend `/write` on the most advanced incomplete section
3. Any section in `revision` state -> recommend `/write <revision section>` to address Overseer directive
4. 2+ sections confirmed -> recommend `/verify`
5. All confirmed -> recommend `/diagnose`
6. Ideation sections exist (no draft sections) -> recommend `/write <ideation section>`

---

## Output Format

```
## Proposal Status: [project name]

Overall: N/M sections confirmed (X%)

### BA Team
[v] Overview (confirmed v3)
[~] Requirements (verifying -- Critic reviewing)

### DA Team
[ ] Data Model (not started)

### TA Team
[>] Architecture (ideation -- 방향 미정)
[!] Cost (revision -- Overseer directive: fix pricing model)

### SA Team
[v] HSM Solution (confirmed v2)
[ ] Implementation Plan (not started)

### Blocked
- ta-architecture depends on sa-hsm (not confirmed yet)
- ta-implementation depends on sa-hsm (not confirmed yet)

### Active Work
- ba-requirements: verifying — Critic reviewing RFP coverage gaps
- ta-cost: revision — Overseer directive issued

### Summary
- 2 confirmed, 1 in progress, 1 revision, 1 ideation, 2 not started
- Next priority: /write ta-cost
```

Then the standard Proposal Guide footer per `reference/proposal-guide-format.md`.

---

## Display Rules

- List teams only if they have at least one SSOT assigned. Skip empty teams.
- If no SSOTs are blocked, omit the **Blocked** section entirely.
- If no SSOTs are active, omit the **Active Work** section entirely.
- The **Summary** line always appears.
- Sections within each team are listed in `meta/outline.yaml` order.
- For `[!]` revision items, always include the Overseer directive text (truncated to ~80 chars if long).
- For `[~]` in-progress items, include the current sub-status when available (e.g., "verifying", "tentative -- user approved, awaiting Overseer").

---

## Error Handling

### Project Not Found

If `meta/proposal-meta.yaml` does not exist:

```
프로젝트가 아직 없습니다. `/design`으로 프로젝트를 먼저 만들어 주세요.
```

Then show the Proposal Guide with recommendation `/design`.

### Outline Not Found

If `meta/outline.yaml` does not exist:

```
outline.yaml을 찾을 수 없습니다. `/design`으로 프로젝트 구조를 정의해 주세요.
```

### No SSOTs Yet

If all sections are `not_started`:

```
## Proposal Status: [project name]

Overall: 0/N sections confirmed (0%)

모든 섹션이 아직 시작되지 않았습니다. 아래 명령어로 작성을 시작하세요.
```

Then Proposal Guide with `/write <first section>` recommendation.

---

## Key References

| File | Purpose |
|------|---------|
| `meta/outline.yaml` | Section ordering, team assignments, dependencies |
| `meta/proposal-meta.yaml` | Project name and metadata |
| `ssot/<team>/<id>.yaml` | Per-section SSOT front-matter (status, version, etc.) |
| `reference/proposal-guide-format.md` | Proposal Guide footer format |
| `reference/state-machine.md` | Valid SSOT states |

---

## Proposal Guide

**Render at the bottom of every response** per `reference/proposal-guide-format.md`.

```
-------------------------------------------------
Project: [project name]
-------------------------------------------------
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
5. All confirmed -> `/diagnose` for final check
6. External input received -> natural language guidance
7. Ideation sections exist -> `/write <section>`
