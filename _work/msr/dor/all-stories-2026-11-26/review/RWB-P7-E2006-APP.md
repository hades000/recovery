# Build-readiness review (script) — RWB-P7-E2006-APP Credit approval pack for NLEADS

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E2006-APP (RWB P7 E2006 APP Credit approval pack for NLEADS v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E2-006 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 16 (7 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'restructuring officer (RW-RESTRUCT) recording on a plan what NLEADS decided, and an internal auditor (RW-AUDIT) reading it afterwards' is in the roles table | — |
| 2 | Links | Pass | §18 has 3 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by 'RWB-P2-E2006-APP', not by a criterion; exception X7 is covered by 'RWB-P3-E2006-APP', not by a criterion; §7 holds 10 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 1 of 9 rules are covered by no criterion and no test case: BR4; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 22 data rows; detcheck: P2 Name `credit_result_at` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-7077 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/decision/v1/approvals/{approvalId}/approve is not in rwb-decision.yaml; P1 POST /api/recovery/decision/v1/approvals/{approvalId}/refuse is not in rwb-decision.yaml; P1 GET /api/recovery/decision/v1/approvals/{approvalId} is not in rwb-decision.yaml; P1 GET /api/recovery/decision/v1/decision-log is not in rwb-decision.yaml (+5 more) | CG-ALL-7078, CG-ALL-7079, CG-ALL-7080, CG-ALL-7081, CG-ALL-7082, CG-ALL-7083, CG-ALL-7084, CG-ALL-7085, CG-ALL-7086, CG-ALL-7087 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P2-009, MSG-P3-005, MSG-P7-006; §14 lists 10 messages; detcheck: P2 MSG-P7-010 is used with another meaning than the standard's; P2 MSG-GEN-006 is used with another meaning than the standard's; P2 MSG-P4-003 is used with another meaning than the standard's | CG-ALL-7088, CG-ALL-7089, CG-ALL-7090 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story | CG-ALL-7092 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7091 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 13 test cases | — |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL12 (assumptions: ASM-0189, ASM-2559, ASM-2608); open decision DL18 (assumptions: ASM-2569, ASM-2839, ASM-2859, ASM-2883); open decision DL19 (assumptions: ASM-1051, ASM-1164, ASM-1809, ASM-1810) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E2006-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7078 | POST /api/recovery/decision/v1/approvals/{approvalId}/approve is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7079 | POST /api/recovery/decision/v1/approvals/{approvalId}/refuse is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7080 | GET /api/recovery/decision/v1/approvals/{approvalId} is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7081 | GET /api/recovery/decision/v1/decision-log is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7082 | GET /api/recovery/decision/v1/decision-log/{entryId} is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7084 | rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1` (shared, the ledger of ADR-022) | X6 | Conflict | Solution architect |
| CG-ALL-7086 | rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision.events.v1` (the service topic of R4) | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7077 | Name `credit_result_at` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7083 | HTTP errors with no message ID: 401 | X5 | Missing | Business analyst |
| CG-ALL-7085 | Payload of rwb.decision.DecisionRecorded.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7087 | Payload of rwb.decision.DecisionRecorded.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7088 | MSG-P7-010 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7089 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7090 | MSG-P4-003 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7091 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7092 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §5 X1: A checklist document is not on the case (covered by 'RWB-P2-E2006-APP' only) | Not specified in the source documents | |
| AC13 | §5 X7: The case is not in AWAITING_CREDIT_APPROVAL, or the treatment is not a restructure (covered by 'RWB-P3-E2006-APP' only) | Not specified in the source documents | |
| AC14 | §8 BR4 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC15 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC16 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
