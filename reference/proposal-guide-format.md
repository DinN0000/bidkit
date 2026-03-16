# Proposal Guide — Rendering Spec

The Proposal Guide is a status footer appended to the bottom of every agent
response. It should help a proposal PM understand the current situation without
needing to know internal role names or raw state-machine terminology.

## Format

Render inside a fenced code block (` ``` `) so lines display consistently across terminals:

```
─────────────────────────────────────────────────
📋 Project: [project name]
─────────────────────────────────────────────────
✅ Done    : [v] section1 (team), [v] section2 (team)
🔄 Current : [~] section3 (team) — activity detail
💡 Next    : /bid:command args — 다음에 할 일 설명
─────────────────────────────────────────────────
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
| 1 | No project | `/bid:design — 새 제안서 프로젝트를 시작합니다` |
| 2 | Design complete, all SSOTs empty | `/bid:write <first priority section> — 첫 번째 섹션 작성을 시작합니다` |
| 3 | Some sections in draft | `/bid:write <incomplete section> — 미완성 섹션을 이어서 작성합니다` |
| 4 | 2+ confirmed | `/bid:diagnose — 품질 진단 및 교차 검증을 수행합니다` |
| 5 | All confirmed | `"최종 출력을 요청해주세요" — 예: "PDF로 출력해줘"` |
| 6 | Output generated, small change needed | Natural language quick edit |
| 7 | Versions available | `"이전 버전이랑 비교해줘"` |
| 8 | External input received | Natural language |
| 9 | Ideation sections exist | `/bid:write <section> — 방향 탐색을 시작합니다` |

## Rules

- Must appear at the bottom of EVERY response from EVERY skill.
- Only ONE recommended action (highest priority from the table above).
- Use commas to separate listed items within a status line.
- Prefer user-facing labels such as `초안 작성 중`, `최종 검토 중`, `수정 필요`.
- Project name is taken from `meta/proposal-meta.yaml` when available.
- Recommended line MUST include both the command and a human-readable explanation separated by ` — `.

## Platform Divergence

The Recommended line is the only place where Claude Code and Codex responses differ:

**Claude Code:**
```
Recommended: /bid:write sa-hsm-001 — HSM 솔루션 초안을 이어서 작성합니다
```

**Codex:**
```
Recommended: "HSM 솔루션 초안 작성을 이어서 진행해주세요" (sa-hsm-001)
```

When rendering Proposal Guide, detect the current platform:
- If CLAUDE.md is the entry point → use `/bid:` command format
- If AGENTS.md is the entry point → use natural language format
