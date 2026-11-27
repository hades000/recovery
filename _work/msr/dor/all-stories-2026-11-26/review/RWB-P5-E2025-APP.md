# Build-readiness review (script) — RWB-P5-E2025-APP Extraction for the stage 2 and 3 document types

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-E2025-APP (RWB P5 E2025 APP Extraction for the stage 2 and 3 document types v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-E2-025 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 13 (4 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer' is in the roles table | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'Access test TC-E2-025-12', not by a criterion; §7 holds 11 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Pass | §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 6 roles | — |
| 7 | Data | Partial | §11 has 25 data rows; detcheck: P2 Name `extraction_method` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `review_only` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `party_names` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-6225, CG-ALL-6226, CG-ALL-6227 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/document/v1/cases/{caseId}/checked-fields is not in rwb-document.yaml; P1 POST /api/recovery/document/v1/intake-items/{intakeItemId}/extract is not published by rwb-document; P1 GET /api/recovery/document/v1/intake-items/{intakeItemId}/extraction is not published by rwb-document; P1 rwb.document.DocumentFieldsExtracted.v1 is on topic rwb.document.events.v1 in the catalog, not rwb.document.events.v1`, with the retry topics at 1 min, 10 min and 1 h and the `.dlt` topic (+1 more) | CG-ALL-6228, CG-ALL-6229, CG-ALL-6230, CG-ALL-6231, CG-ALL-6232 |
| 9 | Messages | Pass | §14 lists 7 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-31 has no empty, loading, error, no access state in the story | CG-ALL-6235, CG-ALL-6236 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6234 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-6233 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-P5-E2025-OPS); 12 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL19 (assumptions: ASM-1051, ASM-1164, ASM-1809, ASM-1810); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355); open decision DL30 (assumptions: ASM-2022, ASM-3378) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P5-E2025-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-agent; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6228 | GET /api/recovery/document/v1/cases/{caseId}/checked-fields is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-6229 | POST /api/recovery/document/v1/intake-items/{intakeItemId}/extract is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-6230 | GET /api/recovery/document/v1/intake-items/{intakeItemId}/extraction is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-6231 | rwb.document.DocumentFieldsExtracted.v1 is on topic rwb.document.events.v1 in the catalog, not rwb.document.events.v1`, with the retry topics at 1 min, 10 min and 1 h and the `.dlt` topic | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6225 | Name `extraction_method` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6226 | Name `review_only` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6227 | Name `party_names` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6232 | Payload of rwb.document.DocumentFieldsExtracted.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6234 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6233 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6235 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6236 | SCR-31 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6237 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §5 X8: A role without Documents R reads the document (covered by 'Access test TC-E2-025-12' only) | Not specified in the source documents | |
| AC13 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC14 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC15 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC16 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
