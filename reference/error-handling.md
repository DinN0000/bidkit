# Error Handling

Guidance for recovering from common error scenarios without blocking overall proposal progress.

## Dependency SSOT Not Yet Created

- **Situation**: A writer needs data from an SSOT that has not been drafted yet.
- **Action**: Proceed with a placeholder value clearly marked as `[PENDING: <ssot-name>]`.
- **Follow-up**: The placeholder is flagged during verification. Once the dependency SSOT reaches `draft` or later, the placeholder must be replaced and the section re-verified.

## Session Interrupted

- **Situation**: The session ends unexpectedly (timeout, crash, user disconnect).
- **Action**: SSOT files on disk are the persistence layer. On next session start, scan all SSOT files and reconstruct state from their front-matter metadata.
- **Follow-up**: Resume from the last completed step. The Proposal Guide will reflect current state automatically.

## Critic Finds Unfixable Issue

- **Situation**: The Critic identifies a problem that the Writer cannot resolve without external input (e.g., missing vendor data, ambiguous RFP requirement).
- **Action**: Escalate to Team Lead, then to user. Do not block other SSOTs — mark this SSOT as `draft` with a note describing the blocker.
- **Follow-up**: Once the user provides the missing information, the Writer revises and re-submits for verification.

## Overseer Review Conflict

- **Situation**: The Overseer disagrees with a Critic-approved section, or two Overseer-level concerns conflict.
- **Action**: Document the disagreement with both positions and supporting evidence. Present to the user for a final decision.
- **Follow-up**: Apply the user's decision, update the SSOT, and re-verify if the change is substantive.

## Rollback

- **Situation**: A confirmed SSOT needs to revert to a previous version (e.g., user realizes the latest edit introduced errors).
- **Action**: Revert the SSOT file to the desired version using git history (`git checkout <commit> -- <file>`).
- **Follow-up**: The reverted SSOT re-enters the state it held at that commit. If it was `confirmed`, it remains `confirmed`. Run `/verify` to ensure consistency with current dependent SSOTs.

## Partial Failure

- **Situation**: One or more SSOTs fail verification or encounter errors while others succeed.
- **Action**: Mark failed SSOTs as `draft`. Continue processing all other teams and SSOTs normally.
- **Follow-up**: Failed SSOTs appear in the Proposal Guide under "In Progress" and are included in the next recommended action.
