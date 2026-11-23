---
title: Smoke_Test
description: Draft smoke-test BRD containing sections 1 and 2 only, focused on recovery case ownership.
status: Draft
---

# Smoke_Test

## 1. Document control

| Field | Value |
|---|---|
| Document | Smoke_Test business requirements document |
| Version | 0.2 |
| Date | 22 November 2026 |
| Author | BRD Builder (AI draft) |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Status | Draft |
| Decision | D-RCV-60 |
| Purpose | Smoke test of the BRD Builder agent |
| Scope of this draft | Sections 1 and 2 only. Sections 3 to 14 of the standard BRD structure, the requirement and rule identifiers (BR-, RULE-, KPI-, Q-) and the traceability appendix are out of scope for this draft and are not started. |
| Supersedes | Version 0.1 of this smoke draft at the same path |
| Reviewers (roles) | Product Owner; Business owner (Recovery); Architecture; Security; Compliance |
| Approval | Not sought. This is a smoke-test draft and carries no approval. No approval status is assumed and none is recorded. |

### Change log

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 22 November 2026 | BRD Builder (AI draft) | First draft. Smoke test: document control and executive summary only, one paragraph on recovery case ownership. |
| 0.2 | 22 November 2026 | BRD Builder (AI draft) | Re-issued smoke draft at the briefed path. Sources re-verified against `requirement/legacy/`; current-state, assignment, data-product, routing and access-scope statements each cited to a named source and section; Decision Log reference moved from v9 to v10 (DL16 unchanged between the two). No identifiers were created, so no traceability rows were added. |

## 2. Executive summary

Today a recovery case has no owner of its own: an account that reaches 90 days past due waits for the weekly manual transfer file at day 91 and is first worked at about day 100, so for about ten days the case has no owner and no clock, and 42 applications hold parts of a case while none of them owns it (Lean BRD, Epic 1 v2, section 1.1 "What is wrong today"). The target operating model replaces this with one owner from day 90 to close, where a case owner holds the case through every route while specialists work tasks on it (Target Operating Model v3, design choices; Business Architecture v4, process owners, L1 process 06 "Take over and own the case", owned by Recovery Strategy with Risk and by the case owner for each case). The case owner is the person who holds the case from day 90 to close and answers for its outcome, expressed as role RW-CASEOWN and recorded on the case as `recovery_case.owner_user_id` (Business Glossary v3, entry "Case owner") [PII]. Ownership is set rather than chosen: the allocation rules set the owner and the queue and start the stage clock (Case and Workflow Model v5, state "Assigned"), and the assignment engine picks the one owner from the assignment rules, favouring continuity and respecting the caseload cap (Feature List v4, FEAT-CWC-08). The ownership facts stay together on the case as state, owner, queue and stage clock, held as the case and ownership data product that the Workbench owns (Case and Workflow Model v5, case data), and the routing rules carry an Owner column in which "Workbench" means that no person holds the case in the next state (Business Rules and Routing Logic v4). The reach of that ownership is bounded: in the pre-release access test a case owner who opens a case owned by another team is returned nothing and the refusal is written to the access log (Admin and Access Model v5, section 10, scope test). The day 90 threshold rests on the ruling that the case owner holds the case from day 90 rather than day 91 (Decision Log v10, DL16). Personal data in this paragraph is classified [PII] because the case owner is identified by a user identifier; no customer records and no financial amounts are reproduced in this document.
