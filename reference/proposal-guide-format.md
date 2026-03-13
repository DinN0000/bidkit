# Proposal Guide — Rendering Spec

The Proposal Guide is a status footer appended to the bottom of every agent
response. It should help a proposal PM understand the current situation without
needing to know internal role names or raw state-machine terminology.

## Format

```
-------------------------------------------------
Project: [project name]
-------------------------------------------------
Current: [user-facing situation label]
Done: [v] section1 (team), [v] section2 (team)
In Progress: [~] section3 (team) -- user-facing activity details
Recommended: /command copy-pasteable example input
-------------------------------------------------
```

## User-Facing Status Labels

| Technical State | User-Facing Label |
|-----------------|-------------------|
| `ideation` | 방향 탐색 중 |
| `draft` | 초안 작성 중 |
| `verifying` | 품질 검토 중 |
| `verified` | 사용자 확인 대기 |
| `tentative` | 최종 검토 대기 |
| `reviewing` | 최종 검토 중 |
| `revision` | 수정 필요 |
| `confirmed` | 확정 |
| absent / not started | 시작 전 |

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

| Priority | Current State | Recommended |
|----------|---|---|
| 1 | No project | /design |
| 2 | Design complete, all SSOTs empty | /write <first priority section> |
| 3 | Some sections in draft | /write on incomplete |
| 4 | 2+ confirmed | /verify |
| 5 | All confirmed | /output to generate final deliverable |
| 6 | Output generated, small change needed | Natural language quick edit |
| 7 | Versions available | /output diff to compare versions |
| 8 | External input received | Natural language |
| 9 | Ideation sections exist | /write <section> |

## Rules

- Must appear at the bottom of EVERY response from EVERY skill.
- Only ONE recommended action (highest priority from the table above).
- Use commas to separate listed items within a status line.
- Prefer user-facing labels such as `초안 작성 중`, `최종 검토 중`, `수정 필요`.
- Project name is taken from `meta/proposal-meta.yaml` when available.
