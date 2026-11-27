# Build-readiness review (script) — RWB-P5-E1054-APP Review queue for low-confidence documents

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-E1054-APP (RWB P5 E1054 APP Review queue for low-confidence documents v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-E1-054 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 21 (11 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 7 Data; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer' is in the roles table | — |
| 2 | Links | Pass | §18 has 21 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X12 is covered by 'Access test TC-E1-054-18', not by a criterion; exception X13 is covered by 'Principle 5 test TC-E1-054-19', not by a criterion; §7 holds 17 owned criteria in Gherkin; §5 has 13 exception paths | — |
| 4 | Business rules | Pass | §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 6 roles | — |
| 7 | Data | Fail | §11 has 23 data rows; detcheck: P1 Index column document.created_at is not a field of document in LDM v9 | CG-ALL-6009 |
| 8 | Contract | Fail | POST `/api/recovery/document/v1/intake-items/{intakeItemId}/resolve` has no idempotency key; PATCH `/api/recovery/document/v1/documents/{documentId}/fields/{fieldId}` has no idempotency key; POST `/api/recovery/document/v1/documents/{documentId}/review` has no idempotency key; detcheck: P1 GET /api/recovery/document/v1/review-items is not in rwb-document.yaml; P1 GET /api/recovery/document/v1/intake-items/{intakeItemId} is not in rwb-document.yaml; P1 GET /api/recovery/document/v1/intake-items/{intakeItemId}/content is not in rwb-document.yaml; P1 POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve is not in rwb-document.yaml (+7 more) | CG-ALL-6010, CG-ALL-6011, CG-ALL-6012, CG-ALL-6013, CG-ALL-6014, CG-ALL-6015, CG-ALL-6016, CG-ALL-6017, CG-ALL-6018, CG-ALL-6019, CG-ALL-6020 |
| 9 | Messages | Partial | §14 lists 13 messages; detcheck: P2 MSG-P4-001 is used with another meaning than the standard's; P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-6021, CG-ALL-6022 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-31 has no empty, loading, error, no access state in the story | CG-ALL-6026, CG-ALL-6027 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6024 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 19 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-6023 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P5-E1032-APP, RWB-P5-E1049-APP); 12 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL19 (assumptions: ASM-1051, ASM-1164, ASM-1809, ASM-1810); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355); open decision DL31 (assumptions: none); detcheck: P2 Open decision DL31 has no assumption | CG-ALL-6029 |
| 19 | Test data | Pass | every test case in §16 names its data (19) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P5-E1054-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P5-E1049-APP, RWB-P5-E1032-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 11 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6009 | Index column document.created_at is not a field of document in LDM v9 | X3 | Conflict | Data |
| CG-ALL-6010 | GET /api/recovery/document/v1/review-items is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-6011 | GET /api/recovery/document/v1/intake-items/{intakeItemId} is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-6012 | GET /api/recovery/document/v1/intake-items/{intakeItemId}/content is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-6013 | POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-6014 | PATCH /api/recovery/document/v1/documents/{documentId}/fields/{fieldId} is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-6015 | POST /api/recovery/document/v1/documents/{documentId}/review is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-6016 | GET /api/recovery/document/v1/documents/{documentId} is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-6017 | GET /api/recovery/case/v1/cases/by-no/{caseNo} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-6018 | rwb-document.yaml holds reviewStatus as a closed enum while the story reads LOV-REVIEW as data | X5 | Conflict | Solution architect |
| CG-ALL-6019 | rwb.document.DocumentFieldsExtracted.v1 is on topic rwb.document.events.v1 in the catalog, not rwb.document.events.v1`, with the retry topics at 1 min, 10 min and 1 h and the `.dlt` topic | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6020 | Payload of rwb.document.DocumentFieldsExtracted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6021 | MSG-P4-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-6022 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-6024 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-6029 | Open decision DL31 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6023 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6025 | Flyway file V1054_1__review_outcome.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6026 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6027 | SCR-31 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6028 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC18. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC18 | §5 X12: The user holds Documents R only (covered by 'Access test TC-E1-054-18' only) | Not specified in the source documents | |
| AC19 | §5 X13: The decision log write fails on attach (covered by 'Principle 5 test TC-E1-054-19' only) | Not specified in the source documents | |
| AC20 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC21 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC22 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
