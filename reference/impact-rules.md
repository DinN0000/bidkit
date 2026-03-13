# Impact Propagation Rules

When a confirmed SSOT is re-edited, the change may cascade to other SSOTs. This document defines how to assess severity, notify stakeholders, and handle cascading re-edits.

## Severity Table

| Severity | Example | Action |
|----------|---------|--------|
| High | Product model change -> price/spec overhaul | Force re-verify all affected SSOTs |
| Medium | Server name change -> possible inconsistency | Notify user, let them decide which SSOTs to re-verify |
| Low | Wording change -> no cross-SSOT impact | Log the change only |

## Determining Severity

1. Read the `affects` metadata array in the modified SSOT's front-matter.
2. For each affected SSOT, classify the change:
   - **High**: the modified field is a primary data point consumed by the affected SSOT (e.g., product model, quantity, price, architecture component).
   - **Medium**: the modified field is referenced but not structurally critical (e.g., hostname, label, descriptive text that appears in another SSOT).
   - **Low**: the modification is purely cosmetic or confined to prose that no other SSOT references.
3. If multiple affected SSOTs exist with different severities, use the highest severity for the overall notification but track per-SSOT severity individually.

## Notification Protocol

| Severity | Who is notified | How |
|----------|----------------|-----|
| High | Overseer -> all affected Team Leads -> user | Automatic. Affected SSOTs transition to `revision` state. |
| Medium | Overseer -> affected Team Leads -> user | Advisory. User decides whether to re-verify. |
| Low | Logged in session history | No active notification. Visible in Proposal Guide if user inspects. |

## Cascading Re-edits

A re-edit of SSOT-A may force revision of SSOT-B, which itself affects SSOT-C. Handle cascades as follows:

1. Build the full dependency graph from `affects` metadata before taking action.
2. Identify the transitive closure of affected SSOTs.
3. Present the full impact list to the user in a single notification — do not fire sequential alerts.
4. Process re-verifications in dependency order (leaves first, then dependents) to avoid redundant work.
5. If a cascade touches more than 5 SSOTs, require explicit user confirmation before proceeding.
