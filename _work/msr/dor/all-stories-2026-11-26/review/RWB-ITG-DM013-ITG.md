# Build-readiness review (script) — RWB-ITG-DM013-ITG Migrate money and closure

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-DM013-ITG (RWB ITG DM013 ITG Migrate money and closure - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-DM-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 10, Fail 7. Detcheck rows: 12 (6 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'data steward' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 5 owned criteria in Gherkin | — |
| 4 | Business rules | Partial | 9 of 9 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9; §8 has 9 rules | — |
| 5 | State transitions | Fail | §9 has 3 transitions; detcheck: P1 Status 'Closed, unchanged' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'Closed, unchanged, and the orphan is listed; matched_to stays empty' in the state table is not a value of LOV-CASE-STATUS; P1 Status 'The break is no longer listed; the closure is unchanged' in the state table is not a value of LOV-CASE-STATUS | CG-ALL-1059, CG-ALL-1060, CG-ALL-1061 |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Partial | §11 has 6 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-1068 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId} is not published by rwb-source-data | CG-ALL-1062, CG-ALL-1063, CG-ALL-1064 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P3 MSG-P1-012 text differs from the Error and Message Standard v4 | CG-ALL-1065, CG-ALL-1066 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-1069 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-DM-013-01-ITG, TC-DM-013-02-ITG, TC-DM-013-03-ITG, TC-DM-013-04-ITG | CG-ALL-1067 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P1-DM013-APP, RWB-P8-DM013-APP); 2 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-DM013-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1059 | Status 'Closed, unchanged' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-1060 | Status 'Closed, unchanged, and the orphan is listed; matched_to stays empty' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-1061 | Status 'The break is no longer listed; the closure is unchanged' in the state table is not a value of LOV-CASE-STATUS | X1 | Conflict | Business analyst |
| CG-ALL-1062 | GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-1063 | GET /api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-1064 | GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId} is not published by rwb-source-data | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1067 | Test cases not in Test Cases v8: TC-DM-013-01-ITG, TC-DM-013-02-ITG, TC-DM-013-03-ITG, TC-DM-013-04-ITG | X9 | Missing | QA |
| CG-ALL-1068 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1065 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1066 | MSG-P1-012 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1069 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-1070 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC6. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC6 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
