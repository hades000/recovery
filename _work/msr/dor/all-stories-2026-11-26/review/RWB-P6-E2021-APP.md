# Build-readiness review (script) — RWB-P6-E2021-APP Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P6-E2021-APP (RWB P6 E2021 APP Letter dispatch loop with proof of delivery from WIN v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-comms |
| Legacy key | RWB-E2-021 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 21 (3 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer (RW-LITOFF)' is in the roles table | — |
| 2 | Links | Pass | §18 has 11 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by AC4, which this story neither owns nor names as owned by another story; exception X3 is covered by AC5, which this story neither owns nor names as owned by another story; §7 holds 8 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 9 of 19 rules are covered by no criterion and no test case: BR11, BR12, BR13, BR14, BR15, BR16, BR17, BR18, BR19; §8 has 19 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 22 data rows; detcheck: P2 Name `party_id` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-6537, CG-ALL-6553 |
| 8 | Contract | Fail | detcheck: P2 HTTP errors with no message ID: 401 no session; P1 rwb-comms.yaml holds deliveryStatus as a closed enum while the story reads LOV-DELIVERY as data; P1 rwb-comms.yaml holds sentType as a closed enum while the story reads LOV-SENT-TYPE as data; P2 Payload of rwb.comms.NoticeDispatched.v1 differs from Kafka Catalog v1 (+5 more) | CG-ALL-6538, CG-ALL-6539, CG-ALL-6540, CG-ALL-6541, CG-ALL-6542, CG-ALL-6543, CG-ALL-6544, CG-ALL-6545, CG-ALL-6546 |
| 9 | Messages | Partial | §14 lists 11 messages; detcheck: P2 MSG-P6-005 is used with another meaning than the standard's; P2 MSG-P3-005 is used with another meaning than the standard's | CG-ALL-6547, CG-ALL-6548 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-04 has no empty, loading, error, no access state in the story; P3 SCR-18 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-6554, CG-ALL-6555, CG-ALL-6556 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6551 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 14 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-6549, CG-ALL-6550 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P6-E1052-APP, RWB-P6-E1055-APP, RWB-P6-E2021-OPS); 11 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P6-E2021-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P6-E1052-APP, RWB-P6-E1055-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6539 | rwb-comms.yaml holds deliveryStatus as a closed enum while the story reads LOV-DELIVERY as data | X5 | Conflict | Solution architect |
| CG-ALL-6540 | rwb-comms.yaml holds sentType as a closed enum while the story reads LOV-SENT-TYPE as data | X5 | Conflict | Solution architect |
| CG-ALL-6543 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6537 | Name `party_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6538 | HTTP errors with no message ID: 401 no session | X5 | Missing | Business analyst |
| CG-ALL-6541 | Payload of rwb.comms.NoticeDispatched.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6542 | Payload of rwb.comms.NoticeDelivered.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6544 | Activity generateLetter is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6545 | Activity conductCheck is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6546 | Activity recordDecision is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6547 | MSG-P6-005 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-6548 | MSG-P3-005 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-6551 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6549 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-6550 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6552 | Flyway file V2021_1__notice_dispatch.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6553 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-6554 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6555 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6556 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6557 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §5 X2: An open X1 or X2 deviation has the contact stop on (covered by AC4, which exist nowhere in this story) | Not specified in the source documents | |
| AC14 | §5 X3: Consent for the postal channel is withdrawn (covered by AC5, which exist nowhere in this story) | Not specified in the source documents | |
| AC15 | §8 BR11, BR12, BR13, BR14, BR15, BR16, BR17, BR18, BR19 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC17 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC18 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
