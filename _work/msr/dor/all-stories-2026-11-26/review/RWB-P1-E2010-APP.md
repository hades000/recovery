# Build-readiness review (script) — RWB-P1-E2010-APP Stage 2 data products: contracts, plans and treatments

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-E2010-APP (RWB P1 E2010 APP Stage 2 data products  contracts, plans and treatments v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-E2-010 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 13 (3 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'recovery developer (RW-TRIBE)' is in the roles table | — |
| 2 | Links | Pass | §18 has 11 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'Section 12.2', not by a criterion; exception X8 is covered by 'Section 12.5', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Pass | §8 has 7 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 9 roles | — |
| 7 | Data | Pass | §11 has 32 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /data-products/{productCode}/records` (the DP04 branch) is not in rwb-source-data.yaml; P1 GET /api/recovery/case/v1/cases/{caseId}/treatments` and the changed-window and active-count reads of the contract is not published by rwb-case; P2 rwb-source-data is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1; P1 Workflow Stage2ProductWorkflow is not in Temporal Catalog v1 (+4 more) | CG-ALL-2399, CG-ALL-2400, CG-ALL-2401, CG-ALL-2402, CG-ALL-2403, CG-ALL-2404, CG-ALL-2405, CG-ALL-2406 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-003; §14 lists 5 messages; detcheck: P3 MSG-P2-006 text differs from the Error and Message Standard v4 | CG-ALL-2407 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-2409, CG-ALL-2410 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-2408 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P1-E1015-APP, RWB-P1-E1069-APP, RWB-P1-E2010-OPS); 11 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL12 (assumptions: ASM-0189, ASM-2559, ASM-2608); open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P1-E2010-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P1-E1069-APP, RWB-P1-E1015-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2399 | GET /data-products/{productCode}/records` (the DP04 branch) is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2400 | GET /api/recovery/case/v1/cases/{caseId}/treatments` and the changed-window and active-count reads of the contract is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-2402 | Workflow Stage2ProductWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2401 | rwb-source-data is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2403 | Activity snapshot(page) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2404 | Activity writeDp04Page is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2405 | Activity checkActiveCount is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2406 | Activity stampDp04 is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2407 | MSG-P2-006 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2408 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2409 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2410 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2411 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X7: The guarantee contract answers with an error or is not deployed yet (covered by 'Section 12.2' only) | Not specified in the source documents | |
| AC10 | §5 X8: The rerun is asked while the workflow of D is running (covered by 'Section 12.5' only) | Not specified in the source documents | |
| AC11 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
