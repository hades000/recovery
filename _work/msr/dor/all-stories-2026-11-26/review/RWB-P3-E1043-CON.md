# Build-readiness review (script) — RWB-P3-E1043-CON Reference data service with versioned tables - contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E1043-CON (RWB P3 E1043 CON Reference data service with versioned tables - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E1-043 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Pass (not applicable) 2, Partial 9, Fail 4. Detcheck rows: 8 (2 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'consumer of the rwb-case reference data' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 7 owned criteria in Gherkin | — |
| 4 | Business rules | Partial | 1 of 12 rules are covered by no criterion and no test case: BR8; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | 8 row(s) of §11 have no BR Field ID; §11 has 8 data rows | — |
| 8 | Contract | Fail | detcheck: P1 rwb-case.yaml holds status as a closed enum while the story reads LOV-VERSION-STATUS as data | CG-ALL-3747 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P4-003; §14 lists 5 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-3748 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-39 has no empty, loading, error, no access state in the story; P3 SCR-40 has no empty, loading, error, no access state in the story; P3 SCR-42 has no empty, loading, error, no access state in the story | CG-ALL-3752, CG-ALL-3753, CG-ALL-3754 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P3-E1043-CON-01, TC-P3-E1043-CON-02, TC-P3-E1043-CON-03, TC-P3-E1043-CON-04, TC-P3-E1043-CON-05, TC-P3-E1043-CON-06, TC-P3-E1043-CON-07; P3 §18 test lists differ from RTM v7 | CG-ALL-3749, CG-ALL-3750 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104) | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_access | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3747 | rwb-case.yaml holds status as a closed enum while the story reads LOV-VERSION-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-3751 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3748 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3749 | Test cases not in Test Cases v8: TC-P3-E1043-CON-01, TC-P3-E1043-CON-02, TC-P3-E1043-CON-03, TC-P3-E1043-CON-04, TC-P3-E1043-CON-05, TC-P3-E1043-CON-06, TC-P3-E1043-CON-07 | X9 | Missing | QA |
| CG-ALL-3750 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3752 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3753 | SCR-40 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3754 | SCR-42 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §8 BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
