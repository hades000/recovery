# Build-readiness review (script) — RWB-ITG-TE004-ITG Masked data in SIT and UAT — integration

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-TE004-ITG (RWB ITG TE004 ITG Masked data in SIT and UAT - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-TE-004 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 9 (3 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'QA integration engineer' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 5 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Pass | §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; §10 has 8 roles | — |
| 7 | Data | Partial | 1 row(s) of §11 have no BR Field ID; §11 has 11 data rows; detcheck: P2 Name `tool_run` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly | CG-ALL-466, CG-ALL-474 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 GET /api/recovery/source-data/v1/customers/{id} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data | CG-ALL-467, CG-ALL-468, CG-ALL-469 |
| 9 | Messages | Partial | §14 lists 3 messages; detcheck: P3 MSG-P2-006 text differs from the Error and Message Standard v4 | CG-ALL-470 |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 13 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-ITG-TE004-01, TC-ITG-TE004-02, TC-ITG-TE004-03, TC-ITG-TE004-04, TC-ITG-TE004-05; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-471, CG-ALL-472, CG-ALL-473 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P1-E1065-APP, RWB-P1-E1069-APP, RWB-PLT-TE004-APP); 3 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-TE004-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-access, rwb-case, rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-467 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-468 | GET /api/recovery/source-data/v1/customers/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-469 | GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-466 | Name `tool_run` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-471 | Test cases not in Test Cases v8: TC-ITG-TE004-01, TC-ITG-TE004-02, TC-ITG-TE004-03, TC-ITG-TE004-04, TC-ITG-TE004-05 | X9 | Missing | QA |
| CG-ALL-474 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-470 | MSG-P2-006 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-472 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-473 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
