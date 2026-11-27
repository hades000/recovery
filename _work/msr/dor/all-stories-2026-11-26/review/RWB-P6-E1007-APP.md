# Build-readiness review (script) — RWB-P6-E1007-APP Integration adapters for outbound files

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P6-E1007-APP (RWB P6 E1007 APP Integration adapters for outbound files v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-comms |
| Legacy key | RWB-E1-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 28 (5 P1). AC review rows: 1. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'platform administrator (RW-PLATADM)' is in the roles table | — |
| 2 | Links | Pass | §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X5 is covered by 'TC-E1-007-04', not by a criterion; exception X10 is covered by 'BR10', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-UNI-33' has no BR ID; rule row 'R-UNI-34' has no BR ID; rule row 'R-UNI-40' has no BR ID; 10 of 13 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 29 data rows; detcheck: P2 Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `interface_run` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `interface_signoff` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-6289, CG-ALL-6290, CG-ALL-6291, CG-ALL-6313 |
| 8 | Contract | Fail | detcheck: P1 GET /file-runs/{businessDate} is not in rwb-comms.yaml; P1 POST /file-runs/{businessDate}/retry is not in rwb-comms.yaml; P1 GET /api/recovery/source-data/v1/customers/{customerId} is not published by rwb-source-data; P2 HTTP errors with no message ID: 401 no session (+10 more) | CG-ALL-6292, CG-ALL-6293, CG-ALL-6294, CG-ALL-6295, CG-ALL-6296, CG-ALL-6297, CG-ALL-6298, CG-ALL-6299, CG-ALL-6300, CG-ALL-6301, CG-ALL-6302, CG-ALL-6303 (+2) |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P7-003; §14 lists 7 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P2 MSG-P2-001 text differs from the Error and Message Standard v4; P3 MSG-P4-003 text differs from the Error and Message Standard v4 | CG-ALL-6306, CG-ALL-6307, CG-ALL-6308 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-44 has no empty, loading, error, no access state in the story; P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-6314, CG-ALL-6315 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6312 |
| 12 | Test cases | Fail | AC5 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC5; P3 §18 test lists differ from RTM v7 | CG-ALL-6309, CG-ALL-6310, CG-ALL-6311 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL06 (assumptions: ASM-0189, ASM-2559, ASM-2608, ASM-2776) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P6-E1007-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6292 | GET /file-runs/{businessDate} is not in rwb-comms.yaml | X5 | Missing | Solution architect |
| CG-ALL-6293 | POST /file-runs/{businessDate}/retry is not in rwb-comms.yaml | X5 | Missing | Solution architect |
| CG-ALL-6294 | GET /api/recovery/source-data/v1/customers/{customerId} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-6297 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6300 | Workflow NoticeFileRunWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 15 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6289 | Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6290 | Name `interface_run` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6291 | Name `interface_signoff` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6295 | HTTP errors with no message ID: 401 no session | X5 | Missing | Business analyst |
| CG-ALL-6296 | Payload of rwb.comms.NoticeDispatched.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6298 | rwb-comms is not a consumer of rwb.integration.FileDelivered.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6299 | rwb-comms is not a consumer of rwb.integration.FileFailed.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6301 | Activity selectFileRecords is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6302 | Activity renderNoticeFile is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6303 | Activity storeNoticeFile is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6304 | Activity handoffFile is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6305 | Activity recordFileRun is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6307 | MSG-P2-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-6310 | Criteria with no test case: AC5 | X9 | Missing | QA |
| CG-ALL-6312 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6306 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-6308 | MSG-P4-003 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-6309 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-6311 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6313 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-6314 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6315 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6316 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC5 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X5: The answer of the source-data contract carries the stale marker of the business date (covered by 'TC-E1-007-04' only) | Not specified in the source documents | |
| AC10 | §5 X10: The decision record cannot be written where a rule decided the eligible set (covered by 'BR10' only) | Not specified in the source documents | |
| AC11 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
