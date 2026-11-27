# Build-readiness review (script) — RWB-P1-E1002-APP Case list v1 with case ID, owner and queue

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-E1002-APP (RWB P1 E1002 APP Case list v1 with case ID, owner and queue v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-E1-002 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 14 (5 P1). AC review rows: 1. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'team manager (RW-TEAMMGR)' is in the roles table | — |
| 2 | Links | Pass | §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by AC5, which this story neither owns nor names as owned by another story; exception X6 is covered by AC10, which this story neither owns nor names as owned by another story; §7 holds 6 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 1 of 10 rules are covered by no criterion and no test case: BR8; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Partial | 8 row(s) of §11 have no BR Field ID; §11 has 8 data rows | — |
| 8 | Contract | Fail | POST `/admin/jobs/{jobId}/rerun` has no idempotency key; detcheck: P1 GET /case-list/dates/{businessDate} is not in rwb-source-data.yaml; P1 GET /case-list/rows is not in rwb-source-data.yaml; P1 GET /api/recovery/case/v1/parameters/{key} is not published by rwb-case; P1 GET /api/recovery/case/v1/reference-data/{lovCode} is not published by rwb-case (+3 more) | CG-ALL-2014, CG-ALL-2015, CG-ALL-2016, CG-ALL-2017, CG-ALL-2018, CG-ALL-2019, CG-ALL-2020 |
| 9 | Messages | Partial | §14 lists 3 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-2021 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no error, no access state in the story | CG-ALL-2025 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2024 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-2022, CG-ALL-2023 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P1-E1002-OPS, RWB-P1-E1015-APP, RWB-P1-E1069-APP); 14 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL17 (assumptions: none); open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602); open decision DL43 (assumptions: ASM-0193, ASM-0737, ASM-0748, ASM-0816); detcheck: P2 Open decision DL17 has no assumption | CG-ALL-2027 |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P1-E1002-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P1-E1069-APP, RWB-P1-E1015-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2014 | GET /case-list/dates/{businessDate} is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2015 | GET /case-list/rows is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2016 | GET /api/recovery/case/v1/parameters/{key} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-2017 | GET /api/recovery/case/v1/reference-data/{lovCode} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-2019 | Workflow CaseListBuildWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2018 | rwb-source-data is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2020 | Activity snapshot(page) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2024 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-2027 | Open decision DL17 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2021 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2022 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-2023 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2025 | SCR-02 has no error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2026 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC6 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §5 X1: A source the case list reads is not COMPLETED at the cut-off (covered by AC5, which exist nowhere in this story) | Not specified in the source documents | |
| AC13 | §5 X6: A case account has no `v_ace_account` row for the business date (covered by AC10, which exist nowhere in this story) | Not specified in the source documents | |
| AC14 | §8 BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC15 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC16 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC17 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
