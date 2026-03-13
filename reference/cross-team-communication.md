# Cross-Team Communication

Four communication channels keep teams synchronized. Each channel has a defined sender, receiver, and trigger.

## Channels

### 1. Dependency Notification

- **Trigger**: An SSOT is modified and its `affects` list includes SSOTs owned by other teams.
- **Flow**: Team Lead (source) -> Team Lead (dependent)
- **Content**: Which SSOT changed, which fields, severity level.
- **Expected response**: Dependent Team Lead reviews impact and decides whether to revise.

### 2. Glossary Sync

- **Trigger**: A new term is added or an existing term is changed in the glossary.
- **Flow**: Critic -> Overseer -> all Team Leads
- **Content**: Term, old definition (if changed), new definition, rationale.
- **Expected response**: Teams update their SSOTs if the term appears in their content.

### 3. Escalation

- **Trigger**: Two or more teams disagree on shared data (e.g., product count, server sizing).
- **Flow**: Team Leads -> Overseer
- **Content**: The conflicting values, each team's justification, source references.
- **Expected response**: Overseer arbitrates per the conflict resolution protocol below.

### 4. Impact Broadcast

- **Trigger**: A confirmed SSOT is re-edited.
- **Flow**: Overseer -> all affected Team Leads
- **Content**: Full impact analysis (see `reference/impact-rules.md`), list of affected SSOTs, required actions.
- **Expected response**: Affected teams acknowledge and begin revision if severity is High.

## Conflict Resolution Protocol

When contradictory data exists across SSOTs:

1. **Overseer detects contradiction.** This may surface during Overseer review, cross-team verification, or user report.

2. **Identify authoritative source.** Ownership rules:
   - SA owns product specifications, solution architecture, and competitive positioning.
   - TA owns infrastructure counts, platform configurations, and deployment topology.
   - BA owns requirements mapping, cost estimation, and process definitions.
   - Researcher owns reference cases and delivery history.
   - If ownership is ambiguous, the Overseer asks the user to designate the authority.

3. **Flag non-authoritative SSOT.** The SSOT that does not own the contested data is marked for revision. Its state transitions to `revision` and it re-enters the verification cycle.

4. **User decides ambiguous cases.** If no clear owner exists or both teams have equal claim, the Overseer presents both values with supporting evidence and the user makes the final call.
