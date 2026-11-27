# Build-readiness review (script) — RWB-ITG-DM005-ITG Migrate contact and promises

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-DM005-ITG (RWB ITG DM005 ITG Migrate contact and promises - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-DM-005 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 10 (3 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'data steward' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 11 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 5 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 7 of 7 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7; §8 has 7 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Partial | role RW-OFF in §10 is not in Users Roles and Permissions v5; §10 has 10 roles | — |
| 7 | Data | Partial | §11 has 4 data rows; detcheck: P2 Field IDs DF-CAS-001 to DF-CAS-055 are not all fields of recovery_case in LDM v9; P2 Criteria and test data read ACE views directly | CG-ALL-992, CG-ALL-998 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/data-products/DP05/records?caseId={caseId} is not published by rwb-source-data; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access | CG-ALL-993, CG-ALL-994, CG-ALL-995 |
| 9 | Messages | Partial | §14 lists 3 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-996 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-999 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 4 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-DM-005-01-ITG, TC-DM-005-02-ITG, TC-DM-005-03-ITG, TC-DM-005-04-ITG | CG-ALL-997 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-P1-DM005-APP); 1 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602); open decision DL29 (assumptions: none); detcheck: P2 Open decision DL29 has no assumption | CG-ALL-1001 |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-DM005-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-993 | GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-994 | GET /api/recovery/source-data/v1/data-products/DP05/records?caseId={caseId} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-995 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-992 | Field IDs DF-CAS-001 to DF-CAS-055 are not all fields of recovery_case in LDM v9 | X3 | Conflict | Data |
| CG-ALL-997 | Test cases not in Test Cases v8: TC-DM-005-01-ITG, TC-DM-005-02-ITG, TC-DM-005-03-ITG, TC-DM-005-04-ITG | X9 | Missing | QA |
| CG-ALL-998 | Criteria and test data read ACE views directly | X12 | Outdated | QA |
| CG-ALL-1001 | Open decision DL29 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-996 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-999 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-1000 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC6. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC6 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
