# Build-readiness review (script) — RWB-P5-E1032-APP Automatic attach from the OCR intake

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-E1032-APP (RWB P5 E1032 APP Automatic attach from the OCR intake v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-E1-032 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 15 (7 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X13 is covered by 'TC-E1-032-17 (Principle 5)', not by a criterion; exception X14 is covered by 'TC-E1-032-16 (Access)', not by a criterion; §7 holds 15 owned criteria in Gherkin; §5 has 14 exception paths | — |
| 4 | Business rules | Pass | §8 has 7 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Partial | §11 has 30 data rows; detcheck: P2 Name `uk_document_case_type_hash` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-5815 |
| 8 | Contract | Fail | POST `/api/recovery/document/v1/intake-items/{intakeItemId}/resolve` has no idempotency key; detcheck: P1 POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve is not in rwb-document.yaml; P1 GET /api/recovery/document/v1/intake-items is not in rwb-document.yaml; P1 GET /api/recovery/document/v1/intake-items/{intakeItemId} is not in rwb-document.yaml; P1 GET /api/recovery/document/v1/intake-items/{intakeItemId}/content is not in rwb-document.yaml (+3 more) | CG-ALL-5816, CG-ALL-5817, CG-ALL-5818, CG-ALL-5819, CG-ALL-5820, CG-ALL-5821, CG-ALL-5822 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-GEN-006; §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-31 has no empty, loading, error, no access state in the story | CG-ALL-5826, CG-ALL-5827 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-5824 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 17 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-5823 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P5-E1024-APP, RWB-P5-E1032-INF, RWB-P5-E1032-OPS); 15 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL21 (assumptions: none); detcheck: P2 Open decision DL21 has no assumption | CG-ALL-5829 |
| 19 | Test data | Pass | every test case in §16 names its data (17) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P5-E1032-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P5-E1024-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5816 | POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5817 | GET /api/recovery/document/v1/intake-items is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5818 | GET /api/recovery/document/v1/intake-items/{intakeItemId} is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5819 | GET /api/recovery/document/v1/intake-items/{intakeItemId}/content is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5820 | GET /api/recovery/case/v1/cases/by-no/{caseNo} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-5821 | rwb-document.yaml holds reviewStatus as a closed enum while the story reads LOV-REVIEW as data | X5 | Conflict | Solution architect |
| CG-ALL-5822 | Event type rwb.document.DocumentAttached.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5815 | Name `uk_document_case_type_hash` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5824 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-5829 | Open decision DL21 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5823 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5825 | Flyway file V1032_1__intake_match.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5826 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5827 | SCR-31 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5828 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §5 X13: The decision log write fails during an attach (covered by 'TC-E1-032-17 (Principle 5)' only) | Not specified in the source documents | |
| AC17 | §5 X14: A role without Documents C attaches an item (covered by 'TC-E1-032-16 (Access)' only) | Not specified in the source documents | |
| AC18 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC19 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC20 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC21 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC22 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
