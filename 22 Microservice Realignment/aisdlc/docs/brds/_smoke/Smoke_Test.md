---
title: Smoke_Test
description: Draft smoke-test BRD for the BRD Builder agent, sections 1 and 2 only, with one paragraph on recovery case ownership.
status: Draft
---
Smoke_Test. BRD Builder smoke test. SCB Collections and Recovery. Henka Group, 22 November 2026

# Smoke_Test

## 1. Document control

| Field | Value |
|---|---|
| Document | Smoke_Test business requirements document |
| Version | 0.3 |
| Date | 22 November 2026 |
| Author | BRD Builder (AI draft) |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Status | Draft |
| Decision | D-RCV-60 |
| Purpose | Smoke test of the BRD Builder agent: confirm the agent reads the legacy sources, writes to the briefed path and holds to a bounded section list |
| Scope of this draft | Sections 1 and 2 only. Sections 3 to 14 of the standard BRD structure are not started, no business requirement, rule, measure, assumption, constraint, dependency, risk or open-question identifiers (BR-, RULE-, KPI-, ASM-, CON-, DEP-, RISK-, Q-) are created, and no traceability rows are added to `requirement/Traceability_Matrix.md` |
| Supersedes | Version 0.2 of this smoke draft at the same path; that version is kept unchanged at `_work/msr/smoke/Smoke_Test_v0.2.md` |
| Reviewers (roles) | Product Owner; Business owner (Recovery); Architecture; Security; Compliance |
| Approval | Not sought and not recorded. This is a smoke-test draft; no approval is assumed and the approval table (section 13 of the standard structure) is not part of this draft |

### Change log

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 22 November 2026 | BRD Builder (AI draft) | First draft. Smoke test: document control and executive summary only, one paragraph on recovery case ownership. |
| 0.2 | 22 November 2026 | BRD Builder (AI draft) | Re-issued smoke draft at the briefed path. Sources re-verified against `requirement/legacy/`; current-state, assignment, data-product, routing and access-scope statements each cited to a named source and section; Decision Log reference moved from v9 to v10 (DL16 unchanged between the two). No identifiers were created, so no traceability rows were added. |
| 0.3 | 22 November 2026 | BRD Builder (AI draft) | D-RCV-60 re-issue of the smoke draft at the briefed path. Version 0.2 preserved unchanged at `_work/msr/smoke/Smoke_Test_v0.2.md` before this version was written. Sections 1 and 2 only, as briefed. Executive summary rewritten as a single paragraph on recovery case ownership and re-grounded in the sources it cites (Lean BRD Epic 1 v3; Business Glossary v3; Target Operating Model v3; Business Architecture v4; Case and Workflow Model v5; Feature List v4; Business Rules and Routing Logic v4; Admin and Access Model v5; Decision Log v10). No identifiers created; no traceability rows added. |

## 2. Executive summary

A recovery case is owned by a person, the case owner, who holds the case from day 90 to close and answers for its outcome (Business Glossary v3, glossary entry "Case owner"). Today that owner is missing at the point where the case begins: an account that reaches 90 days past due waits for the weekly manual transfer file at day 91 and is first worked at about day 100, so for about ten days the case has no owner and no clock, and 42 applications hold parts of a case and none owns it (Lean BRD, Epic 1 v3, section 1.1 "What is wrong today"). The target operating model replaces that gap with one owner from day 90 to close, a case owner who holds the case through every route while specialists work tasks on it (Target Operating Model v3, design choices; Business Architecture v4, process owners, L1 process 06 "Take over and own the case", owned by Recovery Strategy with Risk and, for each case, by the case owner). Ownership is set rather than chosen by the person who holds it: when the allocation rules set the owner and the queue, the case reaches the status "Assigned" and the stage clock starts (Case and Workflow Model v5, case status "Assigned"), and the assignment engine picks the one owner for the case from the assignment rules, favouring continuity and respecting the caseload cap (Feature List v4, FEAT-CWC-08). The facts that make the ownership readable sit together: state, owner, queue and stage clock are held as the "Case and ownership" case file item that the Workbench keeps (Case and Workflow Model v5, case file items), they are carried by the role RW-CASEOWN and stored on the case as `recovery_case.owner_user_id` (Business Glossary v3, glossary entry "Case owner") [PII], and the routing rules record who holds the case in the next state in an Owner column in which "Workbench" means that no person holds it (Business Rules and Routing Logic v4, routing rules). The reach of that ownership is bounded and is tested before each release: a case owner who opens a case owned by another team is returned nothing and the refusal is written to the access log (Admin and Access Model v5, section 10, scope test), and the day 90 starting point rests on the entry-threshold ruling that a case enters recovery at 90 days past due rather than at 91 (Decision Log v10, DL16).
