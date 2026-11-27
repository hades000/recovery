# Build-readiness review (script) — RWB-P3-E1019-APP Roles, teams and queues as data

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E1019-APP (RWB P3 E1019 APP Roles, teams and queues as data v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E1-019 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 7 (3 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'reference data administrator (RW-REFADM)' is in the roles table | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'Access test TC-E1-019-13', not by a criterion; exception X11 is covered by 'Not a legacy AC; TC-P3-E1019-CON-04 covers the 503', not by a criterion; exception X12 is covered by 'Not a legacy AC; TC-P3-E1019-DB-06 covers the rollback', not by a criterion; §7 holds 12 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 1 of 9 rules are covered by no criterion and no test case: BR7; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 3 transitions | — |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Pass | §11 has 12 data rows | — |
| 8 | Contract | Fail | detcheck: P1 rwb-case.yaml holds assignmentMethod as a closed enum while the story reads LOV-ASSIGN as data; P1 rwb-case.yaml holds status as a closed enum while the story reads LOV-VERSION-STATUS as data | CG-ALL-3490, CG-ALL-3491 |
| 9 | Messages | Pass | §14 lists 6 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-42 has no empty, loading, error, no access state in the story | CG-ALL-3495 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 13 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-3492 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-P3-E1019-DB); 11 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL01 (assumptions: ASM-0189, ASM-1230, ASM-1770, ASM-1988); open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P3-E1019-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_access | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3490 | rwb-case.yaml holds assignmentMethod as a closed enum while the story reads LOV-ASSIGN as data | X5 | Conflict | Solution architect |
| CG-ALL-3491 | rwb-case.yaml holds status as a closed enum while the story reads LOV-VERSION-STATUS as data | X5 | Conflict | Solution architect |
| CG-ALL-3493 | Java package th.co.scb.ace.workbench.recovery.case.queues uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3492 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3494 | Flyway file V019_1__queue_member.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3495 | SCR-42 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3496 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §5 X10: A role without Reference data C loads a file (covered by 'Access test TC-E1-019-13' only) | Not specified in the source documents | |
| AC14 | §5 X11: The rwb-access contract does not answer inside 2 s (covered by 'Not a legacy AC; TC-P3-E1019-CON-04 covers the 503' only) | Not specified in the source documents | |
| AC15 | §5 X12: The queue applies but the member replace fails (covered by 'Not a legacy AC; TC-P3-E1019-DB-06 covers the rollback' only) | Not specified in the source documents | |
| AC16 | §8 BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
