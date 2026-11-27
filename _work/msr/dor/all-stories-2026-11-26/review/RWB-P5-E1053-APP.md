# Build-readiness review (script) — RWB-P5-E1053-APP Field extraction for the six types into the index

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-E1053-APP (RWB P5 E1053 APP Field extraction for the six types into the index v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-E1-053 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 14 (2 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner' is in the roles table | — |
| 2 | Links | Pass | §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by 'Access test TC-E1-053-14', not by a criterion; §7 holds 13 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 1 of 10 rules are covered by no criterion and no test case: BR10; §8 has 10 rules | — |
| 5 | State transitions | Fail | §9 has 7 transitions; detcheck: P1 The story adds EXTRACT_MAX_ATTEMPTS to the closed list LOV-INTAKE-REVIEW; P1 The story adds EXTRACT_TIMEOUT_SECONDS to the closed list LOV-INTAKE-REVIEW | CG-ALL-5982, CG-ALL-5983 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 6 roles | — |
| 7 | Data | Partial | §11 has 19 data rows; detcheck: P2 Name `extraction_method` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `review_only` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `owner_name` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `borrower_name` is not a field or entity in LDM v9 or Data Classification v5 (+1 more) | CG-ALL-5984, CG-ALL-5985, CG-ALL-5986, CG-ALL-5987, CG-ALL-5988 |
| 8 | Contract | Partial | detcheck: P2 Payload of rwb.document.DocumentFieldsExtracted.v1 differs from Kafka Catalog v1 | CG-ALL-5989 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-31 has no empty, loading, error, no access state in the story | CG-ALL-5993, CG-ALL-5994 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-5991 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 14 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-5990 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P5-E1025-APP, RWB-P5-E1049-APP); 10 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL19 (assumptions: ASM-1051, ASM-1164, ASM-1809, ASM-1810); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355); open decision DL33 (assumptions: ASM-0135, ASM-0140, ASM-0890) | — |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P5-E1053-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P5-E1049-APP, RWB-P5-E1025-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5982 | The story adds EXTRACT_MAX_ATTEMPTS to the closed list LOV-INTAKE-REVIEW | X1 | Conflict | Product owner |
| CG-ALL-5983 | The story adds EXTRACT_TIMEOUT_SECONDS to the closed list LOV-INTAKE-REVIEW | X1 | Conflict | Product owner |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5984 | Name `extraction_method` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5985 | Name `review_only` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5986 | Name `owner_name` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5987 | Name `borrower_name` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5988 | Name `guarantor_name` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5989 | Payload of rwb.document.DocumentFieldsExtracted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-5991 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5990 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5992 | Flyway file V1053_1__document_extraction.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5993 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5994 | SCR-31 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5995 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC14. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC14 | §5 X9: A user without Documents R reads the document (covered by 'Access test TC-E1-053-14' only) | Not specified in the source documents | |
| AC15 | §8 BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC16 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC17 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC18 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
