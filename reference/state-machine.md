# SSOT State Machine

## Terminology Note: Three Kinds of "Verification"

This project uses three distinct verification concepts. To avoid confusion, use the specific names below:

| Concept | Performed By | When | Scope |
|---------|-------------|------|-------|
| **Critic Verification** | Critic agent | Session loop steps (5) and (7) | Per-SSOT quality check — RFP coverage, data accuracy, glossary compliance, cross-SSOT data consistency |
| **Overseer Cross-Review** | Overseer agent | Session loop step (10), automatically triggered when SSOT reaches `tentative` | Cross-SSOT consistency — terminology, numeric, naming, strategic alignment across all related SSOTs |
| **`/verify` Command** | Overseer agent | User-invoked | Comprehensive cross-cutting analysis across all `confirmed` and `tentative` SSOTs — broader than a single cross-review |

When referring to these, prefer the specific name (e.g., "Critic Verification" or "Overseer Cross-Review") rather than the generic word "verification."

## State Diagram

```
existing --+
            v
ideation -> draft -> verifying -> verified -> tentative -> reviewing -> confirmed
                        |                                      |
                        +-- fail --> draft (revise)             |
                                                               +-- directive --> revision -> verifying
```

## State Transitions

Each transition with its session loop step reference:

| From | To | Trigger | Session Loop Step |
|------|----|---------|-------------------|
| existing | (enters flow) | loaded from prior proposal | step (5) |
| ideation | draft | direction established | -- |
| draft | verifying | writer completes draft | step (5) |
| verifying | verified | critic passes | step (7) |
| verified | tentative | user approves | step (8)/(9) |
| tentative | reviewing | queued for Overseer | step (10) |
| reviewing | confirmed | Overseer passes | -- |
| reviewing | revision | Overseer directive | returns to step (6) |
| verifying | draft | critic fails | back to step (6) |

## Auto-Detect Mode Table

| SSOT State | Mode | Entry Point |
|-----------|------|-------------|
| Empty / ideation | Create | Session loop from (1) |
| draft | Edit | Session loop from (6) |
| verified / tentative | Revise | Session loop from (6), re-verification |
| confirmed | Re-edit | Warning + impact analysis, then (6) |
| existing | Enhance | Session loop from (5) |

## Impact Propagation Rules

When a confirmed SSOT is modified, changes may affect other SSOTs listed in `affects`. Severity determines the action:

| Severity | Example | Action |
|----------|---------|--------|
| High | Product model change | Force re-verify affected SSOTs |
| Medium | Server name change | Notify user, let them decide |
| Low | Wording change | Log only |
