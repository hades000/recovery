# Build-readiness review (script) — RWB-ITG-E1023-ITG Case record view v1, read only

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1023-ITG (RWB ITG E1023 ITG Case record view v1, read only - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-023 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 10, Fail 7. Detcheck rows: 12 (3 P1). AC review rows: 10. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'QA integration engineer' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 18 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'TC-E1-023-05-ITG, regression for RWB-P3-E1023-APP', not by a criterion; exception X7 is covered by 'TC-E1-023-10-ITG, regression for RWB-P3-E1023-APP', not by a criterion; §7 holds 11 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 10 of 18 rules are covered by no criterion and no test case: BR6, BR10, BR11, BR12, BR13, BR14, BR15, BR16, BR17, BR18; §8 has 18 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 11 roles | — |
| 7 | Data | Partial | §11 has 14 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-281 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/deviation/v1/deviations?caseId={caseId} is not published by rwb-deviation; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 GET /api/recovery/access/v1/me/permissions is not published by rwb-access | CG-ALL-273, CG-ALL-274, CG-ALL-275 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-276 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story | CG-ALL-282 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC13 has no test case in §16; AC14 has no test case in §16; AC15 has no test case in §16; AC16 has no test case in §16; AC17 has no test case in §16; AC18 has no test case in §16; AC19 has no test case in §16; AC20 has no test case in §16; §16 has 13 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-023-12-ITG, TC-E1-023-13-ITG; P3 Test cases listed for criteria this story does not own; P2 Criteria with no test case: AC13, AC14, AC15, AC16, AC17, AC18, AC19, AC20; P3 §18 test lists differ from RTM v7 | CG-ALL-277, CG-ALL-278, CG-ALL-279, CG-ALL-280 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 7 build dependencies are not done yet (RWB-P1-E1068-APP, RWB-P1-E1069-APP, RWB-P3-E1023-APP, RWB-P4-E1023-APP, RWB-P4-E1039-APP, RWB-P5-E1024-APP); 7 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Partial | detcheck: P2 List LOV-CONTACT-TYPE is not in Reference Data v5 | CG-ALL-272 |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1023-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-access, rwb-case, rwb-deviation, rwb-document, rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-273 | GET /api/recovery/deviation/v1/deviations?caseId={caseId} is not published by rwb-deviation | X5 | Missing | Solution architect |
| CG-ALL-274 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-275 | GET /api/recovery/access/v1/me/permissions is not published by rwb-access | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-272 | List LOV-CONTACT-TYPE is not in Reference Data v5 | X4 | Missing | Business analyst |
| CG-ALL-277 | Test cases not in Test Cases v8: TC-E1-023-12-ITG, TC-E1-023-13-ITG | X9 | Missing | QA |
| CG-ALL-279 | Criteria with no test case: AC13, AC14, AC15, AC16, AC17, AC18, AC19, AC20 | X9 | Missing | QA |
| CG-ALL-281 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-276 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-278 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-280 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-282 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-283 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC13 | no test case in §16 |  |
| AC14 | no test case in §16 |  |
| AC15 | no test case in §16 |  |
| AC16 | no test case in §16 |  |
| AC17 | no test case in §16 |  |
| AC18 | no test case in §16 |  |
| AC19 | no test case in §16 |  |
| AC20 | no test case in §16 |  |
| AC4 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC12 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC21. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC21 | §5 X2: The case is outside the caller's scope (covered by 'TC-E1-023-05-ITG, regression for RWB-P3-E1023-APP' only) | Not specified in the source documents | |
| AC22 | §5 X7: The case has no documents and no contact history (covered by 'TC-E1-023-10-ITG, regression for RWB-P3-E1023-APP' only) | Not specified in the source documents | |
| AC23 | §8 BR6, BR10, BR11, BR12, BR13, BR14, BR15, BR16, BR17, BR18 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
