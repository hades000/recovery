# Build-readiness review (script) — RWB-P3-E1002-APP Case list v1 with case ID, owner and queue

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E1002-APP (RWB P3 E1002 APP Case list v1 with case ID, owner and queue v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E1-002 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 6, Fail 6. Detcheck rows: 16 (3 P1). AC review rows: 1. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'team manager (RW-TEAMMGR)' is in the roles table | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 11 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 1 of 10 rules are covered by no criterion and no test case: BR8; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Pass | §11 has 28 data rows | — |
| 8 | Contract | Fail | detcheck: P1 Workflow CaseListDayOpen is not in Temporal Catalog v1; P2 Activity readFreshness is not in Temporal Catalog v1; P2 Activity raiseStaleListAlert is not in Temporal Catalog v1 | CG-ALL-3360, CG-ALL-3361, CG-ALL-3362 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P2 MSG-P1-001 text differs from the Error and Message Standard v4; P2 MSG-P4-001 is used with another meaning than the standard's; P2 MSG-GEN-007 is used with another meaning than the standard's; P2 MSG-GEN-002 is used with another meaning than the standard's (+1 more) | CG-ALL-3363, CG-ALL-3364, CG-ALL-3365, CG-ALL-3366, CG-ALL-3367 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story | CG-ALL-3372 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-3368 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL16 (assumptions: ASM-1094, ASM-5264); open decision DL17 (assumptions: none); open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602); open decision DL31 (assumptions: none); detcheck: P2 Open decision DL17 has no assumption; P2 Open decision DL31 has no assumption | CG-ALL-3374, CG-ALL-3375 |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P3-E1002-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3360 | Workflow CaseListDayOpen is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3369 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-3370 | Java package th.co.scb.ace.workbench.recovery.case.caselist uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3361 | Activity readFreshness is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3362 | Activity raiseStaleListAlert is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3363 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3364 | MSG-P4-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3365 | MSG-GEN-007 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3366 | MSG-GEN-002 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3367 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3374 | Open decision DL17 has no assumption | X2 | Ambiguous | Product owner |
| CG-ALL-3375 | Open decision DL31 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3368 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3371 | Flyway file V012_1__case_list_index.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3372 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3373 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC6 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §8 BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC13 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.
