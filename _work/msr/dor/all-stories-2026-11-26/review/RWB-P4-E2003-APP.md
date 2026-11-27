# Build-readiness review (script) — RWB-P4-E2003-APP Customer's other products on the case

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E2003-APP (RWB P4 E2003 APP Customer's other products on the case v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E2-003 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 6, Fail 6. Detcheck rows: 8 (0 P1). AC review rows: 1. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'compliance and PDPA officer (RW-COMPLY), a case owner (RW-CASEOWN), a team manager (RW-TEAMMGR), a phone collector (RW-PHONECOL) and a platform administrator (RW-PLATADM)' is in the roles table | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X4 is covered by 'BR2', not by a criterion; exception X5 is covered by 'BR2', not by a criterion; exception X6 is covered by 'BR9', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 6 exception paths | — |
| 4 | Business rules | Partial | 1 of 10 rules are covered by no criterion and no test case: BR9; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Pass | §10 has 13 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-REF-039; §11 has 10 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-5152 |
| 8 | Contract | Pass | — | — |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story | CG-ALL-5153 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-5150 |
| 12 | Test cases | Fail | AC8 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC8; P3 §18 test lists differ from RTM v7 | CG-ALL-5147, CG-ALL-5148, CG-ALL-5149 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL20 (assumptions: ASM-0189, ASM-2559, ASM-2608); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355); open decision DL43 (assumptions: ASM-0193, ASM-0737, ASM-0748, ASM-0816) | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P4-E2003-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5148 | Criteria with no test case: AC8 | X9 | Missing | QA |
| CG-ALL-5150 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-5152 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5147 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-5149 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5151 | Flyway file V2003_1__other_products_masking.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5153 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5154 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC8 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X4: The masking rows cannot be read (covered by 'BR2' only) | Not specified in the source documents | |
| AC10 | §5 X5: A request names a field ID the masking catalogue does not carry (covered by 'BR2' only) | Not specified in the source documents | |
| AC11 | §5 X6: The feature switch of this capability is off (covered by 'BR9' only) | Not specified in the source documents | |
| AC12 | §8 BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
