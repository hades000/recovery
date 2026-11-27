# Build-readiness review (script) — RWB-P4-E1065-APP Sandbox database with synthetic recovery data

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E1065-APP (RWB P4 E1065 APP Sandbox database with synthetic recovery data v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E1-065 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 7, Fail 8. Detcheck rows: 15 (5 P1). AC review rows: 1. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'security administrator (RW-SECADM), a reference data administrator (RW-REFADM) and a squad member with a Workbench role (RW-TRIBE)' is in the roles table | — |
| 2 | Links | Partial | §18 names no feature; §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 3 of 10 rules are covered by no criterion and no test case: BR2, BR7, BR8; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 14 data rows; detcheck: P2 Field IDs DF-REF-034 to DF-REF-039 are not all fields of role in LDM v9; P2 Field IDs DF-REF-039 are not all fields of role in LDM v9; P2 Criteria and test data read ACE views directly | CG-ALL-5105, CG-ALL-5106, CG-ALL-5117 |
| 8 | Contract | Fail | detcheck: P1 POST /authorise is not in rwb-access.yaml; P1 GET /me/permissions is not in rwb-access.yaml; P1 rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data; P1 rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | CG-ALL-5108, CG-ALL-5109, CG-ALL-5111, CG-ALL-5112 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-43 has no empty, loading, error, no access state in the story | CG-ALL-5118 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC7 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC7; P3 §18 test lists differ from RTM v7 | CG-ALL-5113, CG-ALL-5114, CG-ALL-5115 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-5110 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL15 (assumptions: ASM-5264); open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL39 (assumptions: ASM-1617, ASM-2705) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Partial | detcheck: P2 List LOV-RISK-TIER is not in Reference Data v5 | CG-ALL-5107 |
| 21 | Contract published | Fail | no contract story RWB-P4-E1065-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_sandbox_read | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5108 | POST /authorise is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5109 | GET /me/permissions is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5110 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-5111 | rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data | X5 | Conflict | Solution architect |
| CG-ALL-5112 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5105 | Field IDs DF-REF-034 to DF-REF-039 are not all fields of role in LDM v9 | X3 | Conflict | Data |
| CG-ALL-5106 | Field IDs DF-REF-039 are not all fields of role in LDM v9 | X3 | Conflict | Data |
| CG-ALL-5107 | List LOV-RISK-TIER is not in Reference Data v5 | X4 | Missing | Business analyst |
| CG-ALL-5114 | Criteria with no test case: AC7 | X9 | Missing | QA |
| CG-ALL-5117 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5113 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-5115 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5116 | Flyway file V1065_1__access_seed.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5118 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5119 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC7 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR2, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
