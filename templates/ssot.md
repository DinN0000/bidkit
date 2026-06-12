---
id: <team>-<name>-<number>    # e.g. sa-hsm-001
title: ""
team: BA | DA | TA | SA
status: existing | ideation | draft | verifying | verified | tentative | reviewing | revision | confirmed
version: 1
parent: null                    # parent SSOT id if split
dependencies: []                # SSOTs this one references
affects: []                     # SSOTs impacted when this changes
scope: ""                       # one-line statement of what this section covers (MECE boundary, set at design time)
not_in_scope: []                # adjacent topics deliberately excluded — list of {topic: "...", owner: <ssot-id>}
verification:
  checklist_passed: 0/0
  critic_issues: []
  user_approved: false
  overseer_approved: false
  overseer_directive: null
history: []
ideation:                       # present only during ideation phase
  notes: null
  direction: null
  alternatives_considered: []
skills_used: []
glossary_terms: []
diagrams: []
---

# [Section Title]

## Summary
> 3-5 bullets (개조식) — conclusions and key numbers only, no Content reuse.

## Content
(Actual proposal content)

## Supporting Evidence
(References, sources from Researcher)

## Verification Log
| Round | Critic Issue | Action | Status |
|-------|-------------|--------|--------|

## Overseer Review Log
| Round | Directive | Action | Status |
|-------|----------|--------|--------|
