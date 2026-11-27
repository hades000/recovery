# Build-readiness review (script) — RWB-P6-E4041-APP Answer a legal or audit document request

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P6-E4041-APP (RWB P6 E4041 APP Answer a legal or audit document request v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-comms |
| Legacy key | RWB-E4-041 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 7, Fail 7. Detcheck rows: 14 (5 P1). AC review rows: 0. Missing criteria: 12.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Pass | §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E4-041-03', not by a criterion; exception X3 is covered by 'BR9', not by a criterion; exception X4 is covered by 'BR9', not by a criterion; exception X5 is covered by 'BR5', not by a criterion; exception X6 is covered by 'BR11', not by a criterion; exception X7 is covered by 'BR11', not by a criterion; exception X8 is covered by 'BR10', not by a criterion; §7 holds 2 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 10 of 14 rules are covered by no criterion and no test case: BR2, BR4, BR5, BR6, BR8, BR10, BR11, BR12, BR13, BR14; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 15 data rows; detcheck: P2 Name `document_request` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `document_request_entry` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `notice_id` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-6760, CG-ALL-6761, CG-ALL-6762 |
| 8 | Contract | Fail | detcheck: P1 POST /cases/{caseId}/document-requests is not in rwb-comms.yaml; P1 GET /document-requests/{requestId} is not in rwb-comms.yaml; P2 HTTP errors with no message ID: 401 no session; 404 the case or the request is absent or out of scope; P1 rwb-comms.yaml holds deliveryStatus as a closed enum while the story reads LOV-DELIVERY as data (+2 more) | CG-ALL-6763, CG-ALL-6764, CG-ALL-6765, CG-ALL-6766, CG-ALL-6767, CG-ALL-6768 |
| 9 | Messages | Pass | §14 lists 6 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-33 has no empty, loading, error, no access state in the story | CG-ALL-6772 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6770 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-041-01, TC-E4-041-02, TC-E4-041-03, TC-E4-041-04 | CG-ALL-6769 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-P6-E4041-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6763 | POST /cases/{caseId}/document-requests is not in rwb-comms.yaml | X5 | Missing | Solution architect |
| CG-ALL-6764 | GET /document-requests/{requestId} is not in rwb-comms.yaml | X5 | Missing | Solution architect |
| CG-ALL-6766 | rwb-comms.yaml holds deliveryStatus as a closed enum while the story reads LOV-DELIVERY as data | X5 | Conflict | Solution architect |
| CG-ALL-6767 | rwb-comms.yaml holds sentType as a closed enum while the story reads LOV-SENT-TYPE as data | X5 | Conflict | Solution architect |
| CG-ALL-6768 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6760 | Name `document_request` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6761 | Name `document_request_entry` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6762 | Name `notice_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6765 | HTTP errors with no message ID: 401 no session; 404 the case or the request is absent or out of scope | X5 | Missing | Business analyst |
| CG-ALL-6769 | Test cases not in Test Cases v8: TC-E4-041-01, TC-E4-041-02, TC-E4-041-03, TC-E4-041-04 | X9 | Missing | QA |
| CG-ALL-6770 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6771 | Flyway file V4041_1__document_request.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6772 | SCR-33 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6773 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | §5 X2: The caller does not hold the Documents right on the case (covered by 'TC-E4-041-03' only) | Not specified in the source documents | |
| AC4 | §5 X3: The request id is unknown, or the case is outside the caller's scope (covered by 'BR9' only) | Not specified in the source documents | |
| AC5 | §5 X4: The case reference is missing from the POST (covered by 'BR9' only) | Not specified in the source documents | |
| AC6 | §5 X5: A notice of the case has no document yet (covered by 'BR5' only) | Not specified in the source documents | |
| AC7 | §5 X6: The rwb-document read does not answer inside 2 s (covered by 'BR11' only) | Not specified in the source documents | |
| AC8 | §5 X7: A produced copy cannot be read from the store (covered by 'BR11' only) | Not specified in the source documents | |
| AC9 | §5 X8: The same POST is repeated with one Idempotency-Key (covered by 'BR10' only) | Not specified in the source documents | |
| AC10 | §8 BR2, BR4, BR5, BR6, BR8, BR10, BR11, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC13 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC14 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
