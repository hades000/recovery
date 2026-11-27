# Build-readiness review (script) — RWB-P6-E1055-APP Proof of delivery capture design with WIN

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P6-E1055-APP (RWB P6 E1055 APP Proof of delivery capture design with WIN v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-comms |
| Legacy key | RWB-E1-055 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 21 (6 P1). AC review rows: 2. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer (RW-LITOFF)' is in the roles table | — |
| 2 | Links | Pass | §18 has 19 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X6 is covered by 'TC-E1-055-09', not by a criterion; exception X9 is covered by 'BR11', not by a criterion; exception X10 is covered by 'BR10', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-LIT-07' has no BR ID; rule row 'R-LIT-08' has no BR ID; rule row 'R-LIT-09' has no BR ID; rule row 'R-UNI-33' has no BR ID; rule row 'R-UNI-34' has no BR ID; rule row 'R-UNI-40' has no BR ID; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 6 roles | — |
| 7 | Data | Partial | §11 has 18 data rows; detcheck: P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-6418, CG-ALL-6419 |
| 8 | Contract | Fail | detcheck: P1 POST /internal/pod-digests is not in rwb-comms.yaml; P1 GET /api/recovery/source-data/v1/data-products/DP07/records is not published by rwb-source-data; P1 rwb-comms.yaml holds deliveryStatus as a closed enum while the story reads LOV-DELIVERY as data; P1 rwb-comms.yaml holds sentType as a closed enum while the story reads LOV-SENT-TYPE as data (+6 more) | CG-ALL-6404, CG-ALL-6405, CG-ALL-6406, CG-ALL-6407, CG-ALL-6408, CG-ALL-6409, CG-ALL-6410, CG-ALL-6411, CG-ALL-6412, CG-ALL-6413 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story; P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-6420, CG-ALL-6421, CG-ALL-6422, CG-ALL-6423 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6416 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-6414, CG-ALL-6415 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P6-E1052-APP, RWB-P6-E1055-INF, RWB-P6-E1055-OPS); 13 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P6-E1055-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P6-E1052-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6404 | POST /internal/pod-digests is not in rwb-comms.yaml | X5 | Missing | Solution architect |
| CG-ALL-6405 | GET /api/recovery/source-data/v1/data-products/DP07/records is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-6406 | rwb-comms.yaml holds deliveryStatus as a closed enum while the story reads LOV-DELIVERY as data | X5 | Conflict | Solution architect |
| CG-ALL-6407 | rwb-comms.yaml holds sentType as a closed enum while the story reads LOV-SENT-TYPE as data | X5 | Conflict | Solution architect |
| CG-ALL-6410 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6411 | Workflow NoticeDispatchWorkflow task queue rwb-comms` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6408 | Payload of rwb.comms.NoticeDispatched.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6409 | Payload of rwb.comms.NoticeDelivered.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6412 | Workflow ID form and start rule of NoticeDispatchWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-6413 | Activity generateLetter is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6416 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-6418 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6414 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-6415 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6417 | Flyway file V1055_1__notice_dispatch.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6419 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-6420 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6421 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6422 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6423 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6424 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC6 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC7 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §5 X6: No barcode three days after sending (covered by 'TC-E1-055-09' only) | Not specified in the source documents | |
| AC13 | §5 X9: A caller or a job reads a path outside `/api/recovery/comms/v1`, or a cross-schema read appears (covered by 'BR11' only) | Not specified in the source documents | |
| AC14 | §5 X10: The decision record cannot be written where a rule decided (covered by 'BR10' only) | Not specified in the source documents | |
| AC15 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC16 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC17 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
