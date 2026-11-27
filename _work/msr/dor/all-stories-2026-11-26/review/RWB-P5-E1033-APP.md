# Build-readiness review (script) — RWB-P5-E1033-APP Search across cases

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-E1033-APP (RWB P5 E1033 APP Search across cases v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-E1-033 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 8, Fail 5. Detcheck rows: 7 (0 P1). AC review rows: 1. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer (RW-LITOFF)' is in the roles table | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'TC-E1-033-11 (Access)', not by a criterion; exception X9 is covered by 'TC-E1-033-02 (target path)', not by a criterion; exception X10 is covered by 'TC-E1-033-04 (target path)', not by a criterion; §7 holds 10 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 1 of 6 rules are covered by no criterion and no test case: BR6; §8 has 6 rules | — |
| 5 | State transitions | Pass | §9 has 3 transitions | — |
| 6 | Authority | Partial | role SY-DOCUMENT in §10 is not in Users Roles and Permissions v5; §10 has 6 roles | — |
| 7 | Data | Partial | §11 has 19 data rows; detcheck: P2 Name `gin_trgm_ops` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `dochub_to_numeric` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-5852, CG-ALL-5853 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Pass | §14 lists 8 messages | — |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-5855 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-5854 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P5-E1024-APP, RWB-P5-E1049-APP); 10 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL19 (assumptions: ASM-1051, ASM-1164, ASM-1809, ASM-1810); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P5-E1024-APP, RWB-P5-E1049-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5852 | Name `gin_trgm_ops` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5853 | Name `dochub_to_numeric` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5855 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5854 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5856 | Flyway file V1_5_033__document_search_indexes.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5857 | Flyway file V1033_1__document_search_indexes.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5858 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC4 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §5 X8: A role without Documents R searches (covered by 'TC-E1-033-11 (Access)' only) | Not specified in the source documents | |
| AC12 | §5 X9: The `rwb-case` case-list read does not answer within 2 s or its breaker is open (covered by 'TC-E1-033-02 (target path)' only) | Not specified in the source documents | |
| AC13 | §5 X10: The `rwb-access` authorise read does not answer within 2 s or its breaker is open (covered by 'TC-E1-033-04 (target path)' only) | Not specified in the source documents | |
| AC14 | §8 BR6 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC15 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
