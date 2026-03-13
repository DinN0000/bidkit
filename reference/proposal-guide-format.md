# Proposal Guide — Rendering Spec

The Proposal Guide is a status footer appended to the bottom of every agent response. It gives the user an at-a-glance view of project progress and a single recommended next action.

## Format

```
-------------------------------------------------
Project: [project name]
-------------------------------------------------
Done: [v] section1 (team), [v] section2 (team)
In Progress: [~] section3 (team) -- current activity details
Recommended: /command copy-pasteable example input
-------------------------------------------------
```

## Status Icons

| Icon | Meaning |
|------|---------|
| [v] | confirmed |
| [~] | in progress (draft / verifying / verified / tentative / reviewing) |
| [>] | ideation |
| [ ] | not started |
| [!] | revision (Overseer directive or re-edit of confirmed) |

## Recommendation Logic

Show exactly ONE recommendation — the highest-priority match from top to bottom:

| Current State | Recommended |
|---|---|
| No project | /design |
| Design complete, all SSOTs empty | /write <first priority section> |
| Some sections in draft | /write on incomplete |
| 2+ confirmed | /verify |
| All confirmed | /diagnose for final check |
| External input received | Natural language |
| Ideation sections exist | /write <section> |

## Rules

- Must appear at the bottom of EVERY response from EVERY skill.
- Only ONE recommended action (highest priority from the table above).
- Use commas to separate listed items within a status line.
- No forced line breaks inside status lines.
- Project name is taken from the active design SSOT.
