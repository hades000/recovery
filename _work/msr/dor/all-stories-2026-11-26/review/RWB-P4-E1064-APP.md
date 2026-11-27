# Build-readiness review (script) — RWB-P4-E1064-APP Data dictionary for the 14 data products

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E1064-APP (RWB P4 E1064 APP Data dictionary for the 14 data products v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E1-064 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 5, Fail 7. Detcheck rows: 15 (4 P1). AC review rows: 2. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'data steward and data product owner (RW-DATASTEW), a reference data administrator (RW-REFADM) and a security administrator (RW-SECADM)' is in the roles table | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 9 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Pass | §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; §10 has 11 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 23 data rows; detcheck: P2 Name `v_data_dictionary` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `ace_view_owner` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly | CG-ALL-5090, CG-ALL-5091, CG-ALL-5101 |
| 8 | Contract | Fail | detcheck: P1 GET /admin/dictionary-authority is not in rwb-access.yaml; P1 POST /admin/dictionary-authority-loads/{loadId}/approve is not in rwb-access.yaml; P1 POST /admin/dictionary-authority-loads/{loadId}/return is not in rwb-access.yaml; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access (+1 more) | CG-ALL-5092, CG-ALL-5093, CG-ALL-5094, CG-ALL-5095, CG-ALL-5096 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P3 MSG-P7-002 text differs from the Error and Message Standard v4 | CG-ALL-5097 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-40 has no empty, loading, error, no access state in the story; P3 SCR-43 has no empty, loading, error, no access state in the story | CG-ALL-5102, CG-ALL-5103 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC6 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC6; P3 §18 test lists differ from RTM v7 | CG-ALL-5098, CG-ALL-5099, CG-ALL-5100 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P4-E1064-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case, rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5092 | GET /admin/dictionary-authority is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5093 | POST /admin/dictionary-authority-loads/{loadId}/approve is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5094 | POST /admin/dictionary-authority-loads/{loadId}/return is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5095 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5090 | Name `v_data_dictionary` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5091 | Name `ace_view_owner` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5096 | HTTP errors with no message ID: 404 unknown load or unknown table code | X5 | Missing | Business analyst |
| CG-ALL-5099 | Criteria with no test case: AC6 | X9 | Missing | QA |
| CG-ALL-5101 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5097 | MSG-P7-002 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-5098 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-5100 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5102 | SCR-40 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5103 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5104 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC6 | no test case in §16 |  |
| AC7 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | error answers 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
