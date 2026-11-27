# Build-readiness review (script) — RWB-P6-E2013-APP Approval routing with the delegation of authority table

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P6-E2013-APP (RWB P6 E2013 APP Approval routing with the delegation of authority table v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-comms |
| Legacy key | RWB-E2-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 5, Fail 8. Detcheck rows: 17 (4 P1). AC review rows: 3. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 7 Data; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'approver, for example the Head of Litigation (RW-HEADLIT)' is in the roles table | — |
| 2 | Links | Pass | §18 has 18 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 6 of 18 rules are covered by no criterion and no test case: BR13, BR14, BR15, BR16, BR17, BR18; §8 has 18 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Fail | §11 has 16 data rows; detcheck: P1 Index column notice.approval_ref is not a field of notice in LDM v9; P1 Index column notice.escalation_level is not a field of notice in LDM v9 | CG-ALL-6469, CG-ALL-6470 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P2 HTTP errors with no message ID: 401 no session; P2 Payload of rwb.comms.NoticeGenerated.v1 differs from Kafka Catalog v1; P2 Payload of rwb.comms.NoticeDispatched.v1 differs from Kafka Catalog v1 (+2 more) | CG-ALL-6471, CG-ALL-6472, CG-ALL-6473, CG-ALL-6474, CG-ALL-6475, CG-ALL-6476 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-GEN-001, MSG-GEN-004, MSG-P7-010; §14 lists 6 messages; detcheck: P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-6477 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-10 has no empty, loading, error, no access state in the story; P3 SCR-11 has no empty, loading, error, no access state in the story | CG-ALL-6483, CG-ALL-6484 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6481 |
| 12 | Test cases | Fail | AC5 has no test case in §16; AC6 has no test case in §16; AC7 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 16 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC5, AC6, AC7; P3 §18 test lists differ from RTM v7 | CG-ALL-6478, CG-ALL-6479, CG-ALL-6480 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL18 (assumptions: ASM-2569, ASM-2839, ASM-2859, ASM-2883); open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569) | — |
| 19 | Test data | Pass | every test case in §16 names its data (16) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P6-E2013-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6469 | Index column notice.approval_ref is not a field of notice in LDM v9 | X3 | Conflict | Data |
| CG-ALL-6470 | Index column notice.escalation_level is not a field of notice in LDM v9 | X3 | Conflict | Data |
| CG-ALL-6471 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-6475 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6472 | HTTP errors with no message ID: 401 no session | X5 | Missing | Business analyst |
| CG-ALL-6473 | Payload of rwb.comms.NoticeGenerated.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6474 | Payload of rwb.comms.NoticeDispatched.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6476 | rwb-comms is not a consumer of rwb.decision.ApprovalRequested.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6477 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-6479 | Criteria with no test case: AC5, AC6, AC7 | X9 | Missing | QA |
| CG-ALL-6481 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6478 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-6480 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6482 | Flyway file V2013_1__comms_escalation_notice.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6483 | SCR-10 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6484 | SCR-11 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6485 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC5 | no test case in §16 |  |
| AC6 | no test case in §16 |  |
| AC7 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | §8 BR13, BR14, BR15, BR16, BR17, BR18 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC17 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC18 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC19 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
